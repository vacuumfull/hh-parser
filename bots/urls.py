from django.urls import path
from bots import views

app_name = 'bots'

urlpatterns = ([
	path('start/<int:pager>', views.start_parser),
])