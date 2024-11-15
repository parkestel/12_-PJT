# 기존 movies.json 데이터에 MTM를 위해 genres 필드 추가해서 배열형태로 genre_tmdb_id 넣기
import csv
import json

# 파일 경로 설정
csv_file_path = "movie_model.csv"  # CSV 파일 경로
json_file_path = "movies.json"  # 기존 JSON 파일 경로
output_json_path = "movies_add_genres.json"  # 결과 JSON 파일 경로

# match 데이터
match = [
{
    "model": "movies.genre",
    "pk": 1,
    "fields": {
        "tmdb_id": 28,
        "name": "Action"
    }
},
{
    "model": "movies.genre",
    "pk": 2,
    "fields": {
        "tmdb_id": 12,
        "name": "Adventure"
    }
},
{
    "model": "movies.genre",
    "pk": 3,
    "fields": {
        "tmdb_id": 16,
        "name": "Animation"
    }
},
{
    "model": "movies.genre",
    "pk": 4,
    "fields": {
        "tmdb_id": 35,
        "name": "Comedy"
    }
},
{
    "model": "movies.genre",
    "pk": 5,
    "fields": {
        "tmdb_id": 80,
        "name": "Crime"
    }
},
{
    "model": "movies.genre",
    "pk": 6,
    "fields": {
        "tmdb_id": 99,
        "name": "Documentary"
    }
},
{
    "model": "movies.genre",
    "pk": 7,
    "fields": {
        "tmdb_id": 18,
        "name": "Drama"
    }
},
{
    "model": "movies.genre",
    "pk": 8,
    "fields": {
        "tmdb_id": 10751,
        "name": "Family"
    }
},
{
    "model": "movies.genre",
    "pk": 9,
    "fields": {
        "tmdb_id": 14,
        "name": "Fantasy"
    }
},
{
    "model": "movies.genre",
    "pk": 10,
    "fields": {
        "tmdb_id": 36,
        "name": "History"
    }
},
{
    "model": "movies.genre",
    "pk": 11,
    "fields": {
        "tmdb_id": 27,
        "name": "Horror"
    }
},
{
    "model": "movies.genre",
    "pk": 12,
    "fields": {
        "tmdb_id": 10402,
        "name": "Music"
    }
},
{
    "model": "movies.genre",
    "pk": 13,
    "fields": {
        "tmdb_id": 9648,
        "name": "Mystery"
    }
},
{
    "model": "movies.genre",
    "pk": 14,
    "fields": {
        "tmdb_id": 10749,
        "name": "Romance"
    }
},
{
    "model": "movies.genre",
    "pk": 15,
    "fields": {
        "tmdb_id": 878,
        "name": "Science Fiction"
    }
},
{
    "model": "movies.genre",
    "pk": 16,
    "fields": {
        "tmdb_id": 10770,
        "name": "TV Movie"
    }
},
{
    "model": "movies.genre",
    "pk": 17,
    "fields": {
        "tmdb_id": 53,
        "name": "Thriller"
    }
},
{
    "model": "movies.genre",
    "pk": 18,
    "fields": {
        "tmdb_id": 10752,
        "name": "War"
    }
},
{
    "model": "movies.genre",
    "pk": 19,
    "fields": {
        "tmdb_id": 37,
        "name": "Western"
    }
}
]


# 기존 JSON 데이터 로드
with open(json_file_path, "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

# 테스트용
json_data = json_data[:20]

# CSV 데이터 로드
csv_data = []
with open(csv_file_path, "r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        csv_data.append({
            "tmdb_id": int(row["tmdbid"]),
            "genres": [genre.strip() for genre in row["genres"].split(",")]
        })

# JSON 데이터에 genres 필드 추가
for item in json_data:
    json_tmdb_id = item["fields"]["tmdb_id"]  # JSON 데이터의 tmdb_id
    matching_genres = []  # 추가할 tmdb_id 저장용
    for row in csv_data:
        if row["tmdb_id"] == json_tmdb_id:
            # CSV의 genres 리스트와 match의 name 매칭
            for genre_name in row["genres"]:
                for match_item in match:
                    if match_item["fields"]["name"] == genre_name:
                        matching_genres.append(match_item["fields"]["tmdb_id"])
    # genres 필드 추가
    item["fields"]["genres"] = matching_genres

# 결과 JSON 데이터 저장
with open(output_json_path, "w", encoding="utf-8") as output_file:
    json.dump(json_data, output_file, ensure_ascii=False, indent=4)

print(f"결과가 {output_json_path}에 저장되었습니다.")




