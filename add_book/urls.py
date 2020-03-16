from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enter_book', views.enter_book, name='enter_book'),
    path('added_book', views.added_book, name='added_book'),
]
