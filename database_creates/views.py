from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Director, Movie
from .serializers import GenreSerialzier, MovieLanguageSerialzier
import requests
import pandas as pd

# TMDB API 키 설정
API_KEY = ""

# TMDB API URL 설정
BASE_URL = "https://api.themoviedb.org/3"
MOVIE_LIST_URL = f"{BASE_URL}/movie/popular"
GENRE_LIST_URL = f"{BASE_URL}/genre/movie/list"
LANGUAGES_LIST_URL = f"{BASE_URL}/configuration/languages"
STARS_LIST_URL = f"{BASE_URL}/person/popular"


# Create your views here.
@api_view(["GET"])
def get_genre(request):
    params = {
        "api_key": API_KEY,
    }
    result = None
    response = requests.get(GENRE_LIST_URL, params=params)
    if response.status_code == 200:
        result = response.json()
    else:
        print(f"Error: {response.status_code}")

    for genre in result["genres"]:
        data = {"tmdb_id": genre["id"], "name": genre["name"]}
        serializer = GenreSerialzier(data=data)
        if serializer.is_valid():
            serializer.save()


def get_movie_language(request):
    params = {
        "api_key": API_KEY,
    }
    result = None
    response = requests.get(LANGUAGES_LIST_URL, params=params)
    if response.status_code == 200:
        result = response.json()
    else:
        print(f"Error: {response.status_code}")

    for language in result:
        if language["name"]:
            data = {"iso_code": language["iso_639_1"], "name": language["name"]}
            serializer = MovieLanguageSerialzier(data=data)
            if serializer.is_valid():
                serializer.save()


def get_stars(request):
    params = {
        "api_key": API_KEY,
    }
    result = None
    response = requests.get(STARS_LIST_URL, params=params)
    if response.status_code == 200:
        result = response.json()
    else:
        print(f"Error: {response.status_code}")

    for star in result["results"]:
        data = {"tmdb_id": star["id"], "name": star["name"]}
        serializer = MovieLanguageSerialzier(data=data)
        if serializer.is_valid():
            serializer.save()


def get_directors(request):
    params = {
        "api_key": API_KEY,
    }
    result = None
    movies = Movie.objects.all()

    DIRECTOR_LIST_URL = "{BASE_URL}/movie/{movie_id}/credits"
    response = requests.get(DIRECTOR_LIST_URL, params=params)

    for movie in movies:
        # TMDB API에서 영화 데이터 가져오기
        response = requests.get(
            BASE_URL.format(tmdb_id=movie.tmdb_id), params={"api_key": TMDB_API_KEY}
        )

        if response.status_code == 200:
            result = response.json()
            director_names = []

            # 감독만 필터링
            for person in result["cast"]:
                if person["job"] == "Director":
                    director_names.append(person["name"])

                    # 감독 모델에 이름 추가 (필요시 새로 생성하거나 이미 있는 감독을 찾을 수 있음)
                    director, created = Director.objects.get_or_create(
                        name=person["name"]
                    )

                    # Movie 모델과 Director 모델의 관계 설정 (ManyToMany 또는 다른 관계 모델에 따라 다를 수 있음)
                    movie.directors.add(director)

            # 변경 사항 저장
            movie.save()
        else:
            print(f"Error fetching data for movie {movie.tmdb_id}")
