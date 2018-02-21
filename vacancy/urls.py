from django.urls import path
from vacancy import views

app_name = 'vacancy'

urlpatterns = ([
	path('api/', views.api),
	path('remove/', views.remove),
	path('<pk>/', views.VacancyView.as_view()),
])