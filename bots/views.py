from django.http.reponse import JsonResponse
from bots.hh import HHSpider


def start_parser(request, pager=0):
    bot  = HHSpider()
