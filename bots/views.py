from django.http.response import JsonResponse
from bots.hh import HHSpider
from vacancy.models import Vacancy


def start_parser(request, pager=1):
	print(pager)
	bot  = HHSpider()
	bot.initial_urls = bot.create_urls(pager)
	bot.run()


def api(request):
	queryset = Vacancy.objects.all().values('title', 'date', 'salary','employer', 'address','experience')
	vacancies = [x for x in queryset]

	return JsonResponse(vacancies, safe=False)


