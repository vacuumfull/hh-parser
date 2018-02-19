import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'headhunter.settings')
 
app = Celery('headhunter')
app.config_from_object('django.conf:settings')

app.conf.timezone = 'Europe/Moscow'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()