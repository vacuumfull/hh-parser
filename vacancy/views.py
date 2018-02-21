from  django.views.generic.detail import DetailView
from  vacancy.models import Vacancy

class VacancyView(DetailView):
	"""Vacancy full view"""
	model = Vacancy
	template_name = 'vacancy.html'