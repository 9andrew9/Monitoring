from django.conf.urls import url
from django.template.backends import django

from . import views

from Dashbord import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^software_development/', views.software_development, name='software_development'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^base/', views.base, name='base'),
    url(r'^about/', views.about, name='about'),
    url(r'^json/', views.json, name='json'),
]