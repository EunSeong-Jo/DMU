import requests
import pandas as pd

# ============================================================
# 서울 열린데이터 광장 API (인증키 없이 사용 가능한 예시)
# 서울시 자치구별 인구 통계 데이터
# ============================================================

# API URL (서울 열린데이터 광장은 키 없이도 일부 데이터 제공)
url = "http://openapi.seoul.go.kr:8088/sample/json/SPOP_LOCAL_RESD_JACHI/1/20/"

print("▶ API 호출 중...")
response = requests.get(url)
print(f"▶ 상태 코드: {response.status_code}")

if response.status_code == 200:
    data = response.json()

    # 데이터 추출 (서울 열린데이터의 응답 구조)
    key = list(data.keys())[0]  # 첫 번째 키가 데이터셋 이름
    items = data[key]["row"]

    df = pd.DataFrame(items)
    print(f"\n▶ DataFrame 크기: {df.shape}")
    print(f"▶ 컬럼 목록: {df.columns.tolist()}")
    print(df.head())

    df.to_csv("seoul_population.csv", index=False, encoding="utf-8-sig")
    print("\n▶ 'seoul_population.csv' 저장 완료!")
else:
    print("▶ API 호출 실패")
