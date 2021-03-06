from django.contrib import admin
from django.urls import path, include
from headhunter.views import IndexView
 
import vacancy.urls
import bots.urls 

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('admin/', admin.site.urls),
	path('parser/', include(bots.urls)),
	path('vacancy/', include(vacancy.urls))
]
