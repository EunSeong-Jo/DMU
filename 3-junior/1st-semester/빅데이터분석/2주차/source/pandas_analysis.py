import pandas as pd

# ──────────────────────────────────────
# 샘플 데이터 생성 (결측치, 이상치 포함)
# ──────────────────────────────────────
data = {
    "상품명": ["노트북", "마우스", "키보드", "모니터", "헤드셋", "웹캠", "태블릿", "스피커"],
    "가격": [1200000, 35000, None, 450000, 89000, None, 800000, 55000],
    "카테고리": ["컴퓨터", "주변기기", "주변기기", "컴퓨터", "주변기기", "주변기기", "컴퓨터", "주변기기"],
    "판매량": [150, 500, 300, 200, None, 120, 80, 350],
    "평점": [4.5, 4.2, 3.8, 4.7, None, 3.5, 4.0, 4.1]
}
df = pd.DataFrame(data)

# ──────────────────────────────────────
# 1단계: 데이터 탐색
# ──────────────────────────────────────
print("=" * 60)
print("1단계: 데이터 탐색")
print("=" * 60)

# 데이터 크기
print(f"\n▶ 데이터 크기: {df.shape[0]}행 × {df.shape[1]}열")

# 처음 5행 확인
print("\n▶ 처음 5행:")
print(df.head())

# 데이터 타입 및 결측치 정보
print("\n▶ 데이터 정보:")
print(df.info())

# 기술통계
print("\n▶ 기술통계 (수치형 컬럼):")
print(df.describe())

# 각 컬럼의 데이터 타입
print("\n▶ 데이터 타입:")
print(df.dtypes)

# 고유값 수
print("\n▶ 컬럼별 고유값 수:")
print(df.nunique())

# 범주형 변수 빈도
print("\n▶ 카테고리별 빈도:")
print(df["카테고리"].value_counts())

# ──────────────────────────────────────
# 2단계: 데이터 전처리
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("2단계: 데이터 전처리")
print("=" * 60)

# ── 결측치 확인 ──
print("\n▶ 결측치 현황:")
print(df.isnull().sum())
print(f"\n▶ 결측치 비율 (%):")
print((df.isnull().sum() / len(df) * 100).round(1))

# ── 결측치 처리 ──
# 가격: 이상치 가능성 있으므로 중앙값으로 대체
df["가격"] = df["가격"].fillna(df["가격"].median())

# 판매량: 평균으로 대체 → 음수 제거 → 정수 변환 (안전한 패턴)
mean_sales = df["판매량"].mean()
df["판매량"] = df["판매량"].fillna(mean_sales)
df["판매량"] = df["판매량"].clip(lower=0).astype("int64")

# 평점: 평균으로 대체 후 소수점 1자리 반올림
df["평점"] = df["평점"].fillna(df["평점"].mean()).round(1)

print("\n▶ 결측치 처리 후:")
print(df.isnull().sum())
print("\n▶ 처리된 데이터:")
print(df)

# ── 데이터 타입 확인 ──
print("\n▶ 데이터 타입:")
print(df.dtypes)

# ── 중복 확인 ──
print(f"\n▶ 중복 행 수: {df.duplicated().sum()}개")

# ── 이상치 탐지 (IQR 방식) ──
Q1 = df["가격"].quantile(0.25)
Q3 = df["가격"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"\n▶ 가격 이상치 탐지:")
print(f"  Q1 = {Q1:,.0f}, Q3 = {Q3:,.0f}, IQR = {IQR:,.0f}")
print(f"  정상 범위: {lower_bound:,.0f} ~ {upper_bound:,.0f}")

outliers = df[(df["가격"] < lower_bound) | (df["가격"] > upper_bound)]
print(f"  이상치 수: {len(outliers)}개")
if len(outliers) > 0:
    print(outliers[["상품명", "가격"]])

# ──────────────────────────────────────
# 3단계: 데이터 가공
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("3단계: 데이터 가공")
print("=" * 60)

# ── 필터링 ──
print("\n▶ 10만원 이상 & 평점 4.0 이상 상품:")
filtered = df[(df["가격"] >= 100000) & (df["평점"] >= 4.0)]
print(filtered[["상품명", "가격", "평점"]])

# ── 정렬 ──
print("\n▶ 가격 내림차순 정렬:")
print(df.sort_values("가격", ascending=False)[["상품명", "가격"]])

# ── 그룹핑 및 집계 ──
print("\n▶ 카테고리별 통계:")
category_stats = df.groupby("카테고리").agg(
    상품수=("상품명", "count"),
    평균가격=("가격", "mean"),
    총판매량=("판매량", "sum"),
    평균평점=("평점", "mean")
).round(1)
print(category_stats)

# ── 특성 엔지니어링 ──
df["매출액"] = df["가격"] * df["판매량"]
df["가격대"] = pd.cut(
    df["가격"],
    bins=[0, 50000, 200000, 500000, float("inf")],
    labels=["저가", "중저가", "중고가", "고가"]
)
df["평점등급"] = df["평점"].apply(
    lambda x: "우수" if x >= 4.5 else ("양호" if x >= 4.0 else "보통")
)

print("\n▶ 최종 데이터프레임:")
print(df.to_string(index=False))

import pandas as pd

# ──────────────────────────────────────
# 샘플 데이터 생성 (결측치, 이상치 포함)
# ──────────────────────────────────────
data = {
    "상품명": ["노트북", "마우스", "키보드", "모니터", "헤드셋", "웹캠", "태블릿", "스피커"],
    "가격": [1200000, 35000, None, 450000, 89000, None, 800000, 55000],
    "카테고리": ["컴퓨터", "주변기기", "주변기기", "컴퓨터", "주변기기", "주변기기", "컴퓨터", "주변기기"],
    "판매량": [150, 500, 300, 200, None, 120, 80, 350],
    "평점": [4.5, 4.2, 3.8, 4.7, None, 3.5, 4.0, 4.1]
}
df = pd.DataFrame(data)

# ──────────────────────────────────────
# 1단계: 데이터 탐색
# ──────────────────────────────────────
print("=" * 60)
print("1단계: 데이터 탐색")
print("=" * 60)

# 데이터 크기
print(f"\n▶ 데이터 크기: {df.shape[0]}행 × {df.shape[1]}열")

# 처음 5행 확인
print("\n▶ 처음 5행:")
print(df.head())

# 데이터 타입 및 결측치 정보
print("\n▶ 데이터 정보:")
print(df.info())

# 기술통계
print("\n▶ 기술통계 (수치형 컬럼):")
print(df.describe())

# 각 컬럼의 데이터 타입
print("\n▶ 데이터 타입:")
print(df.dtypes)

# 고유값 수
print("\n▶ 컬럼별 고유값 수:")
print(df.nunique())

# 범주형 변수 빈도
print("\n▶ 카테고리별 빈도:")
print(df["카테고리"].value_counts())

# ──────────────────────────────────────
# 2단계: 데이터 전처리
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("2단계: 데이터 전처리")
print("=" * 60)

# ── 결측치 확인 ──
print("\n▶ 결측치 현황:")
print(df.isnull().sum())
print(f"\n▶ 결측치 비율 (%):")
print((df.isnull().sum() / len(df) * 100).round(1))

# ── 결측치 처리 ──
# 가격: 이상치 가능성 있으므로 중앙값으로 대체
df["가격"] = df["가격"].fillna(df["가격"].median())

# 판매량: 평균으로 대체 → 음수 제거 → 정수 변환 (안전한 패턴)
mean_sales = df["판매량"].mean()
df["판매량"] = df["판매량"].fillna(mean_sales)
df["판매량"] = df["판매량"].clip(lower=0).astype("int64")

# 평점: 평균으로 대체 후 소수점 1자리 반올림
df["평점"] = df["평점"].fillna(df["평점"].mean()).round(1)

print("\n▶ 결측치 처리 후:")
print(df.isnull().sum())
print("\n▶ 처리된 데이터:")
print(df)

# ── 데이터 타입 확인 ──
print("\n▶ 데이터 타입:")
print(df.dtypes)

# ── 중복 확인 ──
print(f"\n▶ 중복 행 수: {df.duplicated().sum()}개")

# ── 이상치 탐지 (IQR 방식) ──
Q1 = df["가격"].quantile(0.25)
Q3 = df["가격"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"\n▶ 가격 이상치 탐지:")
print(f"  Q1 = {Q1:,.0f}, Q3 = {Q3:,.0f}, IQR = {IQR:,.0f}")
print(f"  정상 범위: {lower_bound:,.0f} ~ {upper_bound:,.0f}")

outliers = df[(df["가격"] < lower_bound) | (df["가격"] > upper_bound)]
print(f"  이상치 수: {len(outliers)}개")
if len(outliers) > 0:
    print(outliers[["상품명", "가격"]])

# ──────────────────────────────────────
# 3단계: 데이터 가공
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("3단계: 데이터 가공")
print("=" * 60)

# ── 필터링 ──
print("\n▶ 10만원 이상 & 평점 4.0 이상 상품:")
filtered = df[(df["가격"] >= 100000) & (df["평점"] >= 4.0)]
print(filtered[["상품명", "가격", "평점"]])

# ── 정렬 ──
print("\n▶ 가격 내림차순 정렬:")
print(df.sort_values("가격", ascending=False)[["상품명", "가격"]])

# ── 그룹핑 및 집계 ──
print("\n▶ 카테고리별 통계:")
category_stats = df.groupby("카테고리").agg(
    상품수=("상품명", "count"),
    평균가격=("가격", "mean"),
    총판매량=("판매량", "sum"),
    평균평점=("평점", "mean")
).round(1)
print(category_stats)

# ── 특성 엔지니어링 ──
df["매출액"] = df["가격"] * df["판매량"]
df["가격대"] = pd.cut(
    df["가격"],
    bins=[0, 50000, 200000, 500000, float("inf")],
    labels=["저가", "중저가", "중고가", "고가"]
)
df["평점등급"] = df["평점"].apply(
    lambda x: "우수" if x >= 4.5 else ("양호" if x >= 4.0 else "보통")
)

print("\n▶ 최종 데이터프레임:")
print(df.to_string(index=False))

# ── 가격대별 매출액 합계 ──
print("\n▶ 가격대별 매출액 합계:")
print(df.groupby("가격대", observed=True)["매출액"].sum().apply(lambda x: f"{x:,.0f}"))
