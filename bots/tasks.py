import base64
import time
from urllib.error import HTTPError
from urllib.request import urlretrieve
from headhunter.celery import app
from django.core.cache import cache
from datetime import timedelta


@app.task(name='bots.tasks.check_events')
def check_events():
	pass

@app.task(name='bots.tasks.save_events')
def save_events():
	pass