import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

# ──────────────────────────────────────
# 이상치가 포함된 상품 데이터
# ──────────────────────────────────────
data = {
    "상품명": ["노트북", "마우스", "키보드", "모니터", "헤드셋", "서버장비"],
    "가격": [120, 3.5, 8, 45, 9, 5000],     # 서버장비(5000)가 극단 이상치
    "판매량": [150, 500, 300, 200, 400, 2],  # 서버장비(2)가 극단 이상치
    "평점": [4.5, 4.2, 3.8, 4.7, 4.1, 4.0]
}
df = pd.DataFrame(data)

# 스케일링 대상 컬럼
cols = ["가격", "판매량", "평점"]
X = df[cols].values

print("=" * 70)
print("원본 데이터")
print("=" * 70)
print(df[["상품명"] + cols].to_string(index=False))

# ──────────────────────────────────────
# 3가지 스케일러 비교
# ──────────────────────────────────────
scalers = {
    "MinMaxScaler (0~1)": MinMaxScaler(),
    "StandardScaler (평균0, 표준편차1)": StandardScaler(),
    "RobustScaler (중앙값/IQR)": RobustScaler()
}

for name, scaler in scalers.items():
    print(f"\n{'=' * 70}")
    print(f"{name}")
    print(f"{'=' * 70}")

    X_scaled = scaler.fit_transform(X)
    df_scaled = pd.DataFrame(X_scaled, columns=cols)
    df_scaled.insert(0, "상품명", df["상품명"])
    print(df_scaled.round(2).to_string(index=False))

# ──────────────────────────────────────
# 핵심 비교: 이상치(서버장비)가 미치는 영향
# ──────────────────────────────────────
print("\n" + "=" * 70)
print("핵심 비교: '가격' 컬럼에서 정상 데이터(노트북~헤드셋)의 분포")
print("=" * 70)

for name, scaler in scalers.items():
    X_scaled = scaler.fit_transform(X)
    normal_range = X_scaled[:5, 0]  # 서버장비 제외한 가격
    print(f"  {name:40s} → 범위: {normal_range.min():.3f} ~ {normal_range.max():.3f}")

print("""
[TIP] 해석:
  - MinMaxScaler: 정상 데이터가 0.000~0.023에 뭉침 (구분 불가!)
  - StandardScaler: 정상 데이터가 -0.2~-0.1에 뭉침 (구분 어려움)
  - RobustScaler: 정상 데이터가 넓게 분포 (구분 가능!) <- 이상치에 강건

-> 이상치가 있을 때는 RobustScaler가 정상 데이터를 가장 잘 구분합니다.
""")

# ──────────────────────────────────────
# 올바른 스케일링 순서 (데이터 누수 방지)
# ──────────────────────────────────────
print("=" * 70)
print("올바른 스케일링 순서 (train/test 분리)")
print("=" * 70)

from sklearn.model_selection import train_test_split

X = df[cols].values
X_train, X_test = train_test_split(X, test_size=0.3, random_state=42)

scaler = StandardScaler()
scaler.fit(X_train)                       # 학습 데이터로만 기준 학습
X_train_scaled = scaler.transform(X_train)  # 학습 데이터 변환
X_test_scaled = scaler.transform(X_test)    # 같은 기준으로 테스트 변환

print(f"  학습 데이터 평균: {X_train_scaled.mean(axis=0).round(2)}")
print(f"  테스트 데이터 평균: {X_test_scaled.mean(axis=0).round(2)}")
print("  → 테스트 데이터의 평균이 0이 아닌 것이 정상 (학습 기준으로 변환했으므로)")
