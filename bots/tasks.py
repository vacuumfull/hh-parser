import base64
import time
from urllib.error import HTTPError
from urllib.request import urlretrieve
from headhunter.celery import app
from datetime import timedelta
from django.core.cache import cache
from vacancy.models import Vacancy


@app.task(name='bots.tasks.save_current_vacancies')
def save_current_vacancies():
	queryset = Vacancy.objects.values('title', 'date')
	vacancies = [x for x in queryset]
	if len(vacancies) > 0:
		cache.set('vacancies', vacancies, 3600*24)


@app.task(name='bots.tasks.start_parser')
def start_parser():
	pass


@app.task(name='bots.tasks.check_with_cache')
def check_with_cache(info):
	vacancies  = cache.get('vacancies')
    if isinstance(events, type(None)):
        save_current_vacancies()
        time.sleep(2)
        vacancies = cache.get('vacancies')
        check_or_update(vacancies, info)
    else if len(vacancies) == 0:
		save_vacancy(info)
	else if len(vacancies) > 0:
       	check_or_update(vacancies, info)


def check_or_update(vacancies, info):
	isFound = False
	for item in vacancies:
		if compare(item, prepare_info(info)) > 0:
			isFound = True
	if isFound is False:
		save_vacancy(info)
		update_cache(info)


def save_vacancy(info):
	Vacancy.objects.create( title=info['title'], description=info['content'],
							image=info['link'], date=info['date'],
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
	cache.set('vacancies', events, 3600*24)
