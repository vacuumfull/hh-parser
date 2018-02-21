from django.views.generic.detail import DetailView
from django.http.response import JsonResponse
from django.core.cache import cache
from vacancy.models import Vacancy

class VacancyView(DetailView):
	"""Vacancy full view"""
	model = Vacancy
	template_name = 'vacancy.html'



def api(request):
	queryset = Vacancy.objects.all().values('id','title', 'date', 'salary','employer', 'address','experience')
	vacancies = [x for x in queryset]

	return JsonResponse(vacancies, safe=False)


def remove(request):
	Vacancy.objects.all().delete()
	cache.set('vacancies', [], 3600*24)

	response = {
		'removed' : True
	}

	return JsonResponse(response, safe=False)