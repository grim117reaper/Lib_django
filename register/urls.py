from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register_feed', views.register_feed, name = 'register_feed'),
]
