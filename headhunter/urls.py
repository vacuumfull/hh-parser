from django.contrib import admin
from django.urls import path, include
from pages.views import IndexView

import pages.urls

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include(pages.urls)),
]
