import base64
import time
from bots.hh import HHGrabber
from django.core.cache import cache
from vacancy.models import Vacancy
from headhunter.celery import app



@app.task(name='bots.tasks.save_current_vacancies')
def save_current_vacancies():
	queryset = Vacancy.objects.values('title', 'employer')
	vacancies = [x for x in queryset]
	cache.set('vacancies', vacancies, 3600*24)


@app.task(name='bots.tasks.init_grab')
def init_grab():
	keyword = 'python'
	page = 0
	load_page.delay(current=page, last=100, keyword=keyword)
	

@app.task(name='bots.tasks.load_full_card')
def load_full_card(preview):
	bot = HHGrabber()
	loaded = bot.load_full_card(preview)
	check_with_cache(loaded)


@app.task(name='bots.tasks.load_page')
def load_page(current, last, keyword):
	uri = '/search/vacancy?clusters=true&area=2\
								&enable_snippets=true&text='+ keyword + '&page=' + str(current)
	print(uri)
	bot = HHGrabber()
	result = bot.load_page(uri, last)

	for item in result['preview_cards']:
		load_full_card.delay(item)
	if result['current_page'] <= result['last_page']:
		load_page.delay(current=result['current_page'], last=result['last_page'], keyword=keyword)
	else:
		finish.delay()

@app.task(name='bots.tasks.finish')
def finish():
	print('Congratulations!')


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
	if type(info) is dict:
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
	prepared = {'title': info['title'], 'employer': info['employer']}
	return prepared


def update_cache(new_info):
	vacancies = cache.get('vacancies')
	vacancies.append(prepare_info(new_info))
	cache.set('vacancies', vacancies, 3600*24)
