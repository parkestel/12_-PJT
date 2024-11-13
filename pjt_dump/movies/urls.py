from django.urls import path
from . import views

urlpatterns = [
    path('get-movies/', views.get_movie),
    path('get-genres/', views.get_genres),
    path('get-star/', views.get_star),
    path('get-ott/', views.get_ott_from_csv),
]
