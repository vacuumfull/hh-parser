from django.urls import path
from bots import views

url_patterns = ([
    path('start/<int:pager>', views.start_parser)
])