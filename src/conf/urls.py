# -- coding: utf-8 --
from django.conf.urls import url, include
from django.contrib import admin

# admin.autodiscover()

urlpatterns = [
    url(r'^', admin.site.urls),
]
