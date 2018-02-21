from bots.hh import HHSpider
from django.http.response import JsonResponse

def start_parser(request, pager=1):
	print(pager)
	bot  = HHSpider()
	bot.initial_urls = bot.create_urls(pager)
	bot.run()
	
	response = {
		'started' : True
	}

	return JsonResponse(response, safe=False)

