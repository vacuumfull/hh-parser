from bots.hh import HHGrabber
from django.http.response import JsonResponse

def start_parser(request, pager=1):
	print(pager)
	bot  = HHGrabber()
	
	
	response = {
		'started' : True
	}

	return JsonResponse(response, safe=False)

