import requests
import time
import csv
from django.shortcuts import render
from .models import Movie, Genre, Star, Ott
from django.http import JsonResponse
import logging

API_KEY = 'my key'
API_URL = 'https://api.themoviedb.org/3/'
MOVIE_URL = f'{API_URL}movie/popular?api_key={API_KEY}'
GENRE_URL = f'{API_URL}genre/movie/list?api_key={API_KEY}'
STAR_URL = f'{API_URL}person/popular?api_key={API_KEY}'
# Create your views here.
def get_movie(request):
    response = requests.get(MOVIE_URL)

    if response.status_code == 200:
        data = response.json()
        movies_data = data.get("results", [])
        for movie_data in movies_data:
            # DB에 저장
            Movie.objects.get_or_create(
                tmdb_id=movie_data["id"],
                defaults={
                    "title": movie_data.get("title", ""),
                    "rank": movie_data.get("vote_average", 0.0),
                    "release_date": movie_data.get("release_date", None),
                    "summary": movie_data.get("overview", ""),
                    "poster_path": movie_data.get("poster_path", ""),
                    "is_adult": movie_data.get("adult", False),
                }
            )
        
        return JsonResponse({"status": "Data saved to DB successfully."})
    
    return JsonResponse({"error": "Failed to retrieve data"}, status=response.status_code)

def get_genres(request):
    response = requests.get(GENRE_URL)  

    if response.status_code == 200:
        data = response.json()
        genres_data = data.get("genres", [])
        for genre_data in genres_data:
            # DB에 저장
            Genre.objects.get_or_create(
                tmdb_id=genre_data["id"],
                name=genre_data["name"],
            )
        return JsonResponse({"status": "Data saved to DB successfully."})
    
    return JsonResponse({"error": "Failed to retrieve data"}, status=response.status_code)

def get_star(request):
    for page in range(1, 200 + 1):
        response = requests.get(f"{STAR_URL}&page={page}")

        if response.status_code == 200:
            data = response.json()
            actors_data = data.get("results", [])
            for actor_data in actors_data:
                # DB에 저장
                Star.objects.get_or_create(
                    tmdb_id=actor_data["id"],
                    name=actor_data["name"]
                )
        
        # 1초에 4번 요청 제한 준수
        if (page % 4) == 0:
            time.sleep(1)

    return JsonResponse({"status": "Data saved to DB successfully."})


logging.basicConfig(filename='error_log.txt', level=logging.ERROR)


def get_ott_from_csv(request):
    csv_file_path = 'movie_model.csv'  # CSV 파일 경로 지정
    request_count = 0  # 요청 횟수 카운터
    
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tmdb_id = row['tmdbid']
            response = requests.get(f"{API_URL}{tmdb_id}/watch/providers", params={"api_key": API_KEY})

            if response.status_code == 404:
                logging.error(f"Invalid tmdb_id {tmdb_id}: {response.json().get('status_message')}")
                continue
            if response.status_code == 200:
                data = response.json()
                kr_data = data.get("results", {}).get("KR", {}).get("flatrate", [])
                
                if not kr_data:
                    continue

                for provider in kr_data:
                    provider_id = provider.get("provider_id")
                    provider_name = provider.get("provider_name")
                    logo_path = provider.get("logo_path")
                    
                    if provider_id and provider_name and logo_path:
                        # DB에 저장
                        Ott.objects.get_or_create(
                            tmdb_id=provider_id,
                            name=provider_name,
                            logo_path=logo_path,
                        )

            else:
                error_message = response.json().get('status_message', 'Unknown error')
                return JsonResponse({"error": f"Failed to retrieve data for tmdb_id {tmdb_id}: {error_message}"}, status=response.status_code)
                
            # 요청 횟수 증가 및 속도 제어
            request_count += 1
            if request_count % 4 == 0:
                time.sleep(1)  # 4번 요청 후 1초 대기

    return JsonResponse({"status": "Data saved to DB successfully."})