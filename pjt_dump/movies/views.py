import requests
import time
import csv
from django.db import transaction
from django.shortcuts import render
from .models import Movie, Genre, Star, Ott, Director
from django.http import JsonResponse
import logging

API_KEY = 'my api key'
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



def get_ott_from_csv(request):
    
    url = f"{API_URL}movie/354912/watch/providers?api_key={API_KEY}"
    
    # API 호출
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        kr_data = data.get("results", {}).get("KR", {})
        
        # flatrate 데이터가 있는 경우
        if "flatrate" in kr_data:
            for provider in kr_data["flatrate"]:
                print(provider)
                # get_or_create 메서드 호출 결과 확인
                instance, created = Ott.objects.get_or_create(
                    tmdb_id=provider.get("provider_id"),
                    name=provider.get("provider_name"),
                    logo_path=provider.get("logo_path"),
                )
                
                # 데이터가 새롭게 저장된 경우와 이미 존재하는 경우를 구분하여 출력
                if created:
                    print(f"Provider '{provider.get('provider_name')}' saved to DB.")
                else:
                    print(f"Provider '{provider.get('provider_name')}' already exists in DB.")
    else:
        print(f"Failed to fetch data for TMDB ID: 354912, Status Code: {response.status_code}")

    return JsonResponse({"status": "Data saved to DB successfully."})

# def get_ott_from_csv(request):
#     csv_file_path = 'movie_model.csv'  # CSV 파일 경로 지정
#     request_count = 0  # 요청 횟수 카운터
    
#     with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
        
#         # 한 트랜잭션 내에서 작업 시작
#         with transaction.atomic():
#             for row in reader:
#                 request_count = 0
#                 tmdb_id = row.get("tmdbid")
#                 # print(f"tmdb_id: {tmdb_id}, type: {type(tmdb_id)}")
#                 # API 요청 URL
#                 url = f"{API_URL}movie/{tmdb_id}/watch/providers?api_key={API_KEY}"
                
#                 # API 호출
#                 response = requests.get(url)
#                 request_count += 1  # 요청 횟수 증가
                
#                 # 요청 제한: 1초에 4번
#                 if request_count % 4 == 0:
#                     time.sleep(1)
#                 else:
#                     time.sleep(0.25)

#                 if response.status_code == 200:
#                     data = response.json()
#                     kr_data = data.get("results", {}).get("KR", {})
                    
#                     # flatrate 데이터가 있는 경우
#                     if "flatrate" in kr_data:
#                         for provider in kr_data["flatrate"]:
#                             Ott.objects.get_or_create(
#                                 tmdb_id=provider.get("provider_id"),
#                                 name=provider.get("provider_name"),
#                                 logo_path=provider.get("logo_path"),
#                             )
#                 else:
#                     print(f"Failed to fetch data for TMDB ID: {tmdb_id}, Status Code: {response.status_code}")

#     return JsonResponse({"status": "Data saved to DB successfully."})



# def import_directors_from_csv(request):
#     file_path='movie_model.csv'
#     with open(file_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             director_names = row['director'].split(',')  # 'director' 열에서 쉼표로 분리
#             for name in director_names:
#                 name = name.strip()  # 이름 앞뒤 불필요한 공백만 제거
#                 # Director 모델에서 name이 이미 존재하는지 확인
#                 if not Director.objects.filter(name=name).exists():
#                     Director.objects.create(name=name)
#                     print(f"{name} 추가됨.")
#                 else:
#                     print(f"{name} 이미 존재함.")

def get_director_from_csv(request):
    file_path = 'movie_model.csv'
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            director_names = row['director'].split(',')
            tmdb_id = int(row['tmdbid'])  # 영화의 tmdb_id 가져오기

            for name in director_names:
                name = name.strip()
                
                # Director 모델에서 name이 이미 존재하는지 확인
                director, created = Director.objects.get_or_create(name=name)
                
                # tmdb_id를 movie_ids 필드에 추가 (중복 방지)
                if tmdb_id not in director.movie_ids:
                    director.movie_ids.append(tmdb_id)
                    director.save()

                if created:
                    print(f"{name} 추가됨.")
                else:
                    print(f"{name} 이미 존재함, 영화 ID 추가됨.")