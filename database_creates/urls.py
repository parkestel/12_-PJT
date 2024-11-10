from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("genre/", views.get_genre),
    path("movie-language/", views.get_movie_language),
]
