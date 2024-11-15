# 기존 movies.json 데이터에 MTM를 위해 otts 필드 추가해서 배열형태로 otts에  넣기
import csv
import json

# 파일 경로 설정
csv_file_path = "movie_ott_mapping.csv"  # CSV 파일 경로
json_file_path = "movies.json"  # 기존 JSON 파일 경로
output_json_path = "movies_add_otts.json"  # 결과 JSON 파일 경로


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
            "tmdb_id": int(row["tmdb_id"]),
            "provider_id": [int(ott.strip()) for ott in row["provider_id"].split(",")]
        })

# JSON 데이터에 otts 필드 추가
for item in json_data:
    json_tmdb_id = item["fields"]["tmdb_id"]  # JSON 데이터의 tmdb_id
    matching_providers = []  # 추가할 provider_id 배열 저장용

    for row in csv_data:
        if row["tmdb_id"] == json_tmdb_id:  # tmdb_id가 같으면
            matching_providers.extend(row["provider_id"])  # provider_id 배열 추가

    # otts 필드 추가 (중복 제거)
    item["fields"]["otts"] = list(set(matching_providers))

# 결과 JSON 데이터 저장
with open(output_json_path, "w", encoding="utf-8") as output_file:
    json.dump(json_data, output_file, ensure_ascii=False, indent=4)

print(f"결과가 {output_json_path}에 저장되었습니다.")




