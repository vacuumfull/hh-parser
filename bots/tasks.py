import base64
import time
from urllib.error import HTTPError
from urllib.request import urlretrieve
from headhunter.celery import app
from django.core.cache import cache
from datetime import timedelta
from django.core.cache import cache




@app.task(name='bots.tasks.check_vacancies')
def check_vacancies():
	pass

@app.task(name='bots.tasks.check_paginate')
def check_paginate():
	pass

@app.task(name='bots.tasks.start_parser')
def start_parser():
	pass

@app.task(name='bots.tasks.save_vacancies')
def save_vacancies():
	pass