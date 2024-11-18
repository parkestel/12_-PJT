import csv

# 기존 CSV 파일 경로와 새로 저장할 CSV 파일 경로
input_file = "movie_model.csv"
output_file = "sample_2122.csv"

# 필터링된 데이터 저장
with open(input_file, "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)
    fieldnames = reader.fieldnames  # 기존 필드명 가져오기
    
    # 새 CSV 파일 작성
    with open(output_file, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()  # 헤더 작성

        # `imdbid_2122` 필드 값이 있는 행만 필터링
        for row in reader:
            if row.get("imdbid_2122"):  # 해당 필드가 비어있지 않은지 확인
                writer.writerow(row)

print(f"필터링된 데이터가 {output_file}에 저장되었습니다.")
