import pandas as pd

# ──────────────────────────────────────
# 1. concat 실습 — 월별 판매 데이터 합치기
# ──────────────────────────────────────
print("=" * 60)
print("1. concat: 같은 구조의 데이터 합치기")
print("=" * 60)

df_jan = pd.DataFrame({
    "날짜": ["2026-01-05", "2026-01-12", "2026-01-25"],
    "상품": ["노트북", "마우스", "키보드"],
    "판매량": [10, 50, 30]
})

df_feb = pd.DataFrame({
    "날짜": ["2026-02-03", "2026-02-14", "2026-02-28"],
    "상품": ["노트북", "모니터", "마우스"],
    "판매량": [15, 8, 45]
})

# 위아래로 합치기
df_all = pd.concat([df_jan, df_feb], ignore_index=True)
print(df_all)
print(f"\n합친 결과: {df_all.shape[0]}행")

# ──────────────────────────────────────
# 2. merge 실습 — 다른 구조의 데이터 합치기
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("2. merge: 공통 키로 결합하기")
print("=" * 60)

# 상품 마스터 정보
df_products = pd.DataFrame({
    "상품코드": ["A01", "A02", "A03", "A04"],
    "상품명": ["노트북", "마우스", "키보드", "모니터"],
    "카테고리": ["컴퓨터", "주변기기", "주변기기", "컴퓨터"]
})

# 판매 이력
df_sales = pd.DataFrame({
    "상품코드": ["A01", "A02", "A01", "A03", "A05"],
    "판매량": [10, 30, 5, 15, 20],
    "날짜": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-01", "2026-01-02"]
})

# inner join (양쪽 모두에 있는 것만)
print("\n▶ inner merge (교집합):")
result_inner = pd.merge(df_products, df_sales, on="상품코드", how="inner")
print(result_inner)
print(f"→ A04(모니터): 판매이력 없어서 제외")
print(f"→ A05: 상품마스터에 없어서 제외")

# left join (왼쪽 기준 — 판매 없는 상품도 유지)
print("\n▶ left merge (왼쪽 기준):")
result_left = pd.merge(df_products, df_sales, on="상품코드", how="left")
print(result_left)
print(f"→ A04(모니터): 판매이력 없지만 NaN으로 유지됨")

# ──────────────────────────────────────
# 3. 결합 후 집계 — 실전 패턴
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("3. 결합 후 카테고리별 총 판매량 집계")
print("=" * 60)

merged = pd.merge(df_products, df_sales, on="상품코드", how="inner")
category_sales = merged.groupby("카테고리")["판매량"].sum()
print(category_sales)
