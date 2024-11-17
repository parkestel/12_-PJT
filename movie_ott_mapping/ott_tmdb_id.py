# 영화 tmdb_id from movie_model.csv, ott provider_id from TMDB API 2가지 열 가진 csv 만들기
import requests
import csv
import time

API_KEY = ''
API_URL = 'https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers?api_key='

csv_file_path = 'movie_model.csv'
output_csv_path = 'movie_ott_mapping.csv'

def fetch_ott_provider(tmdb_id):
    url = f"{API_URL}{API_KEY}"
    response = requests.get(url.format(tmdb_id=tmdb_id))
    
    if response.status_code == 200:
        data = response.json()
        kr_data = data.get("results", {}).get("KR", {})
        
        if "flatrate" in kr_data:
            provider_ids = [str(provider.get("provider_id")) for provider in kr_data["flatrate"]]
            return ",".join(provider_ids)  # 쉼표로 구분된 문자열로 변환
    return None

def create_provider_csv():
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
            fieldnames = ['tmdb_id', 'provider_id']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()


            for row in reader:   
                tmdb_id = row['tmdbid']
                provider_ids = fetch_ott_provider(tmdb_id)
                
                if provider_ids:
                    writer.writerow({'tmdb_id': tmdb_id, 'provider_id': provider_ids})
                    print(f"tmdb_id {tmdb_id} - Providers found and written to CSV")
                else:
                    print(f"tmdb_id {tmdb_id} - No providers found, skipping")
                
                # 초당 4회 제한을 맞추기 위해 0.25초 대기
                time.sleep(0.25)

create_provider_csv()
