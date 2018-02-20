from django.urls import path
from vacancy import views

app_name = 'vacancy'

urlpatterns = ([
	path('vacancy/', views.VacancyView)
])