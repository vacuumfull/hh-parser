from django.views.generic import TemplateView


class IndexView(TemplateView):
	"""Вид главной страницы"""
	template_name = 'main.html'