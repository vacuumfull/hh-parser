import base64
import time
from urllib.error import HTTPError
from urllib.request import urlretrieve
from datetime import timedelta
from django.core.cache import cache
from vacancy.models import Vacancy
from headhunter.celery import app



@app.task(name='bots.tasks.save_current_vacancies')
def save_current_vacancies():
	queryset = Vacancy.objects.values('title', 'employer')
	vacancies = [x for x in queryset]
	cache.set('vacancies', vacancies, 3600*24)


@app.task(name='bots.tasks.parse_next_page')
def parse_next_page(page, limit):
	newpage = page + 1
	print('Текущая страница ', newpage)


@app.task(name='bots.tasks.check_with_cache')
def check_with_cache(info):
	vacancies  = cache.get('vacancies')
	if isinstance(vacancies, type(None)):
		save_current_vacancies()
		time.sleep(2)
		vacancies = cache.get('vacancies')
		check_or_update(vacancies, info)
	elif len(vacancies) == 0:
		save_vacancy(info)
		prepared = [prepare_info(info)]
		cache.set('vacancies', prepared, 3600*24)
	elif len(vacancies) > 0:
		check_or_update(vacancies, info)


def check_or_update(vacancies, info):
	isFound = False
	for item in vacancies:
		if compare(item, prepare_info(info)) > 0:
			isFound = True
	if isFound is False:
		save_vacancy(info)
		update_cache(info)


def compare(dict1, dict2):
	diff = set(dict1.items()) & set(dict2.items())
	return len(diff)


def save_vacancy(info):
	Vacancy.objects.create( title=info['title'], content=info['content'],
							link=info['link'], date=info['date'],
							salary=info['salary'], employer=info['employer'],
							address=info['address'], experience=info['experience'])


def prepare_info(info):
	"""Удаляем лишние ключи для сравнения"""
	info_copy = info.copy()
	info_copy.pop('date', None)
	info_copy.pop('content', None)
	info_copy.pop('address', None)
	info_copy.pop('location', None)
	info_copy.pop('salary', None)
	info_copy.pop('experience', None)
	return info_copy


def update_cache(new_info):
	vacancies = cache.get('vacancies')
	vacancies.append(prepare_info(new_info))
	cache.set('vacancies', vacancies, 3600*24)
