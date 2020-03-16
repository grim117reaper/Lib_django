from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check_pass', views.check_pass, name='check_pass'),
    ]
