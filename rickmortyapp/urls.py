from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'rickmorty'
urlpatterns = [
    path('', views.index, name='index'),
    path('episode/<int:id>', views.episode),
    path('character/<int:id>', views.character),
    path('location/<int:id>', views.location),
    url(r'^search', views.search)
]

