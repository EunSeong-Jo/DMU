import pandas as pd

# 서울시 공공자전거 이용정보 데이터 로드
df = pd.read_csv("서울특별시 공공자전거 이용정보(월별)_25.1-6.csv", encoding="cp949")

# 상위 5행 확인
print("=" * 60)
print("서울시 공공자전거 이용정보 (2025년 1~6월)")
print("=" * 60)
print(f"\n데이터 크기: {df.shape[0]}행 x {df.shape[1]}열\n")
print("[ 컬럼 목록 ]")
print(df.columns.tolist())
print(f"\n[ 상위 5행 ]")
print(df.head())
print(f"\n[ 데이터 타입 ]")
print(df.dtypes)

# 1만행까지만 잘라서 저장
df_10k = df.head(10000)
df_10k.to_csv("서울특별시_공공자전거_이용정보_10000.csv", index=False, encoding="utf-8-sig")
print(f"\n1만행 데이터 저장 완료: 서울특별시_공공자전거_이용정보_10000.csv")
