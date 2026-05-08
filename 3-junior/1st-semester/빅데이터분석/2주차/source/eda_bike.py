import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 0. 기본 설정
# ============================================================
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 1단계: 데이터 로드 및 구조 확인
# ============================================================
print("=" * 60)
print("1단계: 데이터 구조 확인")
print("=" * 60)

# 원본 CSV 파일 로드 (cp949 인코딩)
df = pd.read_csv("서울특별시 공공자전거 이용정보(월별)_25.1-6.csv", encoding="cp949")

# 컬럼명이 깨질 경우를 대비하여 직접 지정
df.columns = [
    "대여일자", "대여소번호", "대여소명", "대여구분코드", "성별",
    "연령대코드", "이용건수", "운동량", "탄소량", "이동거리(M)", "이용시간(분)"
]

# 기본 정보 출력
print(f"\n▶ 데이터 크기: {df.shape[0]:,}행 × {df.shape[1]}열")
print(f"\n▶ 컬럼 목록:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i}. {col}")

print(f"\n▶ 데이터 타입:")
print(df.dtypes)

print(f"\n▶ 처음 5행:")
print(df.head())

print(f"\n▶ 마지막 5행:")
print(df.tail())

# 결측치 확인
print(f"\n▶ 컬럼별 결측치 수:")
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(1)
missing_df = pd.DataFrame({"결측치 수": missing, "비율(%)": missing_pct})
print(missing_df[missing_df["결측치 수"] > 0])  # 결측치가 있는 컬럼만 출력

# 숫자로 변환 불가능한 값 확인 (운동량, 탄소량)
print(f"\n▶ 숫자 변환 불가능한 값 확인 (운동량, 탄소량):")
for col in ["운동량", "탄소량"]:
    non_numeric = df[col][pd.to_numeric(df[col], errors="coerce").isna() & df[col].notna()]
    if len(non_numeric) > 0:
        print(f"   [{col}] 비정상 값: {non_numeric.unique()} → {len(non_numeric):,}건")
        print(f"         원인: DB에서 NULL을 '\\N' 문자열로 내보내어 object 타입이 됨")
    else:
        print(f"   [{col}] 비정상 값 없음")

# ============================================================
# 2단계: 데이터 전처리
# ============================================================
print("\n" + "=" * 60)
print("2단계: 데이터 전처리")
print("=" * 60)

# 수치형 변환 (문자열로 저장된 경우 대비)
numeric_candidates = ["이용건수", "운동량", "탄소량", "이동거리(M)", "이용시간(분)"]
for col in numeric_candidates:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 성별 통일 (대소문자 혼용 정리: 'm'->'M', 'f'->'F')
df["성별"] = df["성별"].str.upper()
print(f"\n▶ 성별 정리 후 고유값: {df['성별'].dropna().unique()}")

# 월 컬럼 생성 (202501 → "1월", ..., 202506 → "6월")
month_map = {202501: "1월", 202502: "2월", 202503: "3월",
             202504: "4월", 202505: "5월", 202506: "6월"}
df["월"] = df["대여일자"].map(month_map)
month_order = [f"{i}월" for i in range(1, 7)]
print(f"▶ 월별 데이터 수:")
print(df["월"].value_counts().reindex([m for m in month_order if m in df["월"].values]))

# ============================================================
# 3단계: 기술통계 분석
# ============================================================
print("\n" + "=" * 60)
print("3단계: 기술통계 분석")
print("=" * 60)

# 기술통계
print(f"\n▶ 기술통계:")
print(df[numeric_candidates].describe().round(2))

# 범주형 변수 빈도 분석
print(f"\n▶ 대여구분코드별 건수:")
print(df["대여구분코드"].value_counts())

print(f"\n▶ 연령대별 건수:")
age_order = ["~10대", "20대", "30대", "40대", "50대", "60대", "70대이상", "기타"]
age_counts = df["연령대코드"].value_counts()
print(age_counts.reindex([a for a in age_order if a in age_counts.index]))

print(f"\n▶ 성별 건수 (결측 제외):")
print(df["성별"].value_counts())

# ============================================================
# 4단계: 시각화
# ============================================================
print("\n" + "=" * 60)
print("4단계: 시각화")
print("=" * 60)

# --- 4-1. 결측치 히트맵 ---
plt.figure(figsize=(12, 5))
sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap="YlOrRd")
plt.title("결측치 히트맵", fontsize=14, fontweight="bold")
plt.xlabel("컬럼")
plt.ylabel("행")
plt.tight_layout()
plt.savefig("bike_01_missing_heatmap.png", dpi=150)
plt.show()
print("▶ 'bike_01_missing_heatmap.png' 저장 완료")

# --- 4-2. 월별 이용건수 비교 (막대그래프) ---
plt.figure(figsize=(10, 5))
monthly = df.groupby("월")["이용건수"].sum()
monthly = monthly.reindex([m for m in month_order if m in monthly.index])

colors = ["#2196F3", "#42A5F5", "#66BB6A", "#4CAF50", "#FF9800", "#F44336"]
bars = plt.bar(monthly.index, monthly.values, color=colors[:len(monthly)])
plt.title("월별 총 이용건수 비교", fontsize=14, fontweight="bold")
plt.xlabel("월")
plt.ylabel("총 이용건수")

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2., height,
             f"{int(height):,}", ha="center", va="bottom", fontweight="bold")

plt.tight_layout()
plt.savefig("bike_02_monthly_usage.png", dpi=150)
plt.show()
print("▶ 'bike_02_monthly_usage.png' 저장 완료")

# --- 4-3. 연령대별 이용건수 (월별 비교) ---
plt.figure(figsize=(10, 6))
age_monthly = df.groupby(["월", "연령대코드"])["이용건수"].sum().unstack("월")
age_monthly = age_monthly.reindex([a for a in age_order if a in age_monthly.index])
age_monthly = age_monthly.reindex(columns=[m for m in month_order if m in age_monthly.columns])

age_monthly.plot(kind="bar", ax=plt.gca(), color=colors[:len(age_monthly.columns)])
plt.title("연령대별 이용건수 (월별 비교)", fontsize=14, fontweight="bold")
plt.xlabel("연령대")
plt.ylabel("총 이용건수")
plt.xticks(rotation=0)
plt.legend(title="월")
plt.tight_layout()
plt.savefig("bike_03_age_usage.png", dpi=150)
plt.show()
print("▶ 'bike_03_age_usage.png' 저장 완료")

# --- 4-4. 성별 이용건수 비교 (파이차트) ---
gender_data = df[df["성별"].notna()]
gender_sum = gender_data.groupby("성별")["이용건수"].sum()
gender_colors = {"M": "#42A5F5", "F": "#EF5350"}

plt.figure(figsize=(7, 5))
plt.pie(
    gender_sum.values,
    labels=[f"{g} ({v:,}건)" for g, v in zip(gender_sum.index, gender_sum.values)],
    colors=[gender_colors.get(g, "gray") for g in gender_sum.index],
    autopct="%1.1f%%",
    startangle=90
)
plt.title("성별 이용건수 비교", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("bike_04_gender_pie.png", dpi=150)
plt.show()
print("▶ 'bike_04_gender_pie.png' 저장 완료")

# --- 4-5. 이용건수·이동거리·이용시간 분포 (히스토그램 + KDE) ---
plot_cols = ["이용건수", "이동거리(M)", "이용시간(분)"]
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, col in enumerate(plot_cols):
    data = df[col].dropna()
    # 이상치 제거 (상위 1% 초과 제외) — 분포를 보기 쉽게
    upper = data.quantile(0.99)
    data_trimmed = data[data <= upper]
    sns.histplot(data_trimmed, kde=True, ax=axes[i], color="steelblue", bins=30)
    axes[i].set_title(f"{col} 분포 (상위 1% 제외)", fontsize=12)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel("빈도")

plt.suptitle("수치형 변수 분포", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("bike_05_distributions.png", dpi=150, bbox_inches="tight")
plt.show()
print("▶ 'bike_05_distributions.png' 저장 완료")

# --- 4-6. 박스플롯 (월별 이동거리 비교) ---
plt.figure(figsize=(8, 5))
# 이상치가 많으므로 상위 1% 제외하여 시각화
upper_dist = df["이동거리(M)"].quantile(0.99)
df_trimmed = df[df["이동거리(M)"] <= upper_dist]

available_months = [m for m in month_order if m in df_trimmed["월"].values]
sns.boxplot(x="월", y="이동거리(M)", data=df_trimmed,
            order=available_months, palette=colors[:len(available_months)])
plt.title("월별 이동거리 분포 (상위 1% 제외)", fontsize=14, fontweight="bold")
plt.xlabel("월")
plt.ylabel("이동거리 (M)")
plt.tight_layout()
plt.savefig("bike_06_boxplot_distance.png", dpi=150)
plt.show()
print("▶ 'bike_06_boxplot_distance.png' 저장 완료")

# ============================================================
# 5단계: 상관관계 분석
# ============================================================
print("\n" + "=" * 60)
print("5단계: 상관관계 분석")
print("=" * 60)

# 분석 대상 수치형 컬럼
corr_cols = ["이용건수", "운동량", "탄소량", "이동거리(M)", "이용시간(분)"]
corr_matrix = df[corr_cols].corr().round(2)

print("\n▶ 상관계수 행렬:")
print(corr_matrix)

# 히트맵 시각화
plt.figure(figsize=(8, 6))
sns.heatmap(
    corr_matrix,
    annot=True,           # 셀 안에 숫자 표시
    cmap="coolwarm",      # 색상: 파란색(-1) ~ 빨간색(+1)
    center=0,             # 0을 기준으로 색상 대칭
    vmin=-1, vmax=1,      # 범위 고정
    square=True,          # 정사각형 셀
    linewidths=0.5,       # 셀 경계선
    fmt=".2f"             # 소수점 2자리
)
plt.title("변수 간 상관관계 히트맵", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("bike_07_correlation_heatmap.png", dpi=150)
plt.show()
print("▶ 'bike_07_correlation_heatmap.png' 저장 완료")

# 강한 상관관계 쌍 출력
print("\n▶ 강한 상관관계 (|r| ≥ 0.5):")
for i in range(len(corr_matrix.columns)):
    for j in range(i + 1, len(corr_matrix.columns)):
        r = corr_matrix.iloc[i, j]
        if abs(r) >= 0.5:
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            direction = "양의 상관" if r > 0 else "음의 상관"
            print(f"   {col1} ↔ {col2}: r = {r} ({direction})")

# ============================================================
# 6단계: 인사이트 도출 (요약)
# ============================================================
print("\n" + "=" * 60)
print("6단계: EDA 인사이트 요약")
print("=" * 60)

monthly_totals = df.groupby("월")["이용건수"].sum()
monthly_totals = monthly_totals.reindex([m for m in month_order if m in monthly_totals.index])

print(f"""
[데이터 개요]
- 전체 데이터: {df.shape[0]:,}행 × {df.shape[1]}열
- 기간: 2025년 {monthly_totals.index[0]} ~ {monthly_totals.index[-1]}
- 결측치가 있는 컬럼: {(df.isnull().sum() > 0).sum()}개 (성별 컬럼에 집중)

[월별 총 이용건수]""")
for month, total in monthly_totals.items():
    print(f"- {month}: {total:,}건")

print(f"""
[발견한 내용]
- 가장 이용이 많은 달: {monthly_totals.idxmax()} ({monthly_totals.max():,}건)
- 가장 이용이 적은 달: {monthly_totals.idxmin()} ({monthly_totals.min():,}건)
- 성별 결측치는 일일권(비회원) 이용자에서 발생 (회원 정보 없음)
- 이용건수, 이동거리, 이용시간은 서로 강한 양의 상관관계

[다음 단계]
- 결측치 처리 방향 결정 (성별 결측 → 비회원 별도 분석)
- 대여소별 인기 순위 분석
- 시계열 분석 확장 (월별 → 일별, 시간대별)
""")
