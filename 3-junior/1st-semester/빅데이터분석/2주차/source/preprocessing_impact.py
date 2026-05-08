import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows: Malgun Gothic)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 1. 원본 데이터 생성 (결측치와 극단적 이상치 포함)
data = {
    "가격": [100, 120, 110, 130, 150, 140, 5000, 10, None, 135], # 5000(이상치), 10(이상치), None(결측치)
    "평점": [4.0, 4.2, 3.8, 4.3, 4.5, 4.1, 1.0, 5.0, 4.0, None]  # 1.0(이상치), 5.0(이상치), None(결측치)
}
df = pd.DataFrame(data)

# ---------------------------------------------------------
# [Step 1] 전처리 전 상관계수 계산
# ---------------------------------------------------------
# 결측치가 있으면 corr()은 해당 행을 제외하고 계산함
corr_before = df.corr().iloc[0, 1]

# ---------------------------------------------------------
# [Step 2] 데이터 전처리 수행
# ---------------------------------------------------------
df_clean = df.copy()

# 1. 결측치 처리 (중앙값으로 대체)
df_clean["가격"] = df_clean["가격"].fillna(df_clean["가격"].median())
df_clean["평점"] = df_clean["평점"].fillna(df_clean["평점"].median())

# 2. 이상치 처리 (IQR 방식 활용)
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]

df_clean = remove_outliers(df_clean, "가격")
df_clean = remove_outliers(df_clean, "평점")

# ---------------------------------------------------------
# [Step 3] 전처리 후 상관계수 계산
# ---------------------------------------------------------
corr_after = df_clean.corr().iloc[0, 1]

# ---------------------------------------------------------
# [Step 4] 결과 시각화 비교
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 전처리 전 산점도
sns.scatterplot(x="가격", y="평점", data=df, ax=axes[0], color='red', s=100)
axes[0].set_title(f"전처리 전 (상관계수: {corr_before:.2f})\n*이상치와 결측치로 인해 관계 왜곡")

# 전처리 후 산점도
sns.regplot(x="가격", y="평점", data=df_clean, ax=axes[1], color='blue', scatter_kws={'s':100})
axes[1].set_title(f"전처리 후 (상관계수: {corr_after:.2f})\n*정제 후 뚜렷한 양의 상관관계 발견")

plt.tight_layout()
plt.show()

print(f"전처리 전 상관계수: {corr_before:.2f}")
print(f"전처리 후 상관계수: {corr_after:.2f}")