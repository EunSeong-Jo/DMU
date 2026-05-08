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

# 앞서 저장한 CSV 파일 로드
df = pd.read_csv("air_quality_seoul.csv")

# 기본 정보 출력
print(f"\n▶ 데이터 크기: {df.shape[0]}행 × {df.shape[1]}열")
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

# ============================================================
# 2단계: 기술통계 분석
# ============================================================
print("\n" + "=" * 60)
print("2단계: 기술통계 분석")
print("=" * 60)

# 수치형 컬럼 자동 감지
# 대기오염 데이터의 수치값이 문자열로 저장되어 있을 수 있으므로 변환
numeric_candidates = ["미세먼지(PM10)", "초미세먼지(PM2.5)", "오존(O3)",
                      "이산화질소(NO2)", "일산화탄소(CO)", "아황산가스(SO2)"]

for col in numeric_candidates:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # 변환 실패 시 NaN

# 기술통계
print(f"\n▶ 기술통계:")
print(df.describe().round(2))

# 범주형 컬럼 빈도 분석
if "측정소" in df.columns:
    print(f"\n▶ 측정소별 데이터 수:")
    print(df["측정소"].value_counts().head(10))

if "PM10등급" in df.columns:
    print(f"\n▶ PM10 등급 분포:")
    grade_map = {"1": "좋음", "2": "보통", "3": "나쁨", "4": "매우나쁨"}
    df["PM10등급_텍스트"] = df["PM10등급"].astype(str).map(grade_map)
    print(df["PM10등급_텍스트"].value_counts())

# ============================================================
# 3단계: 시각화
# ============================================================
print("\n" + "=" * 60)
print("3단계: 시각화")
print("=" * 60)

# --- 3-1. 결측치 히트맵 ---
plt.figure(figsize=(12, 5))
sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap="YlOrRd")
plt.title("결측치 히트맵", fontsize=14, fontweight="bold")
plt.xlabel("컬럼")
plt.ylabel("행")
plt.tight_layout()
plt.savefig("01_missing_heatmap.png", dpi=150)
plt.show()
print("▶ '01_missing_heatmap.png' 저장 완료")

# --- 3-2. 수치형 변수 분포 (히스토그램 + KDE) ---
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

if len(numeric_cols) > 0:
    # 서브플롯으로 한 번에 표시
    n_cols = min(3, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 4 * n_rows))
    if n_rows * n_cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, col in enumerate(numeric_cols):
        sns.histplot(df[col].dropna(), kde=True, ax=axes[i], color="steelblue")
        axes[i].set_title(f"{col} 분포", fontsize=12)
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("빈도")

    # 빈 서브플롯 숨기기
    for j in range(len(numeric_cols), len(axes)):
        axes[j].set_visible(False)

    plt.suptitle("수치형 변수 분포", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig("02_distributions.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("▶ '02_distributions.png' 저장 완료")

# --- 3-3. 박스플롯 (이상치 확인) ---
if len(numeric_cols) > 0:
    fig, axes = plt.subplots(1, min(4, len(numeric_cols)),
                              figsize=(5 * min(4, len(numeric_cols)), 5))
    if min(4, len(numeric_cols)) == 1:
        axes = [axes]

    for i, col in enumerate(numeric_cols[:4]):
        sns.boxplot(y=df[col].dropna(), ax=axes[i], color="lightcoral")
        axes[i].set_title(f"{col}", fontsize=12)

    plt.suptitle("박스플롯 — 이상치 확인", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("03_boxplots.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("▶ '03_boxplots.png' 저장 완료")

# --- 3-4. 막대그래프 (범주형 변수) ---
if "PM10등급_텍스트" in df.columns:
    plt.figure(figsize=(8, 5))
    grade_order = ["좋음", "보통", "나쁨", "매우나쁨"]
    available_grades = [g for g in grade_order if g in df["PM10등급_텍스트"].values]

    colors = {"좋음": "#2196F3", "보통": "#4CAF50", "나쁨": "#FF9800", "매우나쁨": "#F44336"}
    grade_counts = df["PM10등급_텍스트"].value_counts()

    bars = plt.bar(
        [g for g in available_grades if g in grade_counts.index],
        [grade_counts[g] for g in available_grades if g in grade_counts.index],
        color=[colors.get(g, "gray") for g in available_grades if g in grade_counts.index]
    )
    plt.title("PM10 등급별 측정소 수", fontsize=14, fontweight="bold")
    plt.xlabel("등급")
    plt.ylabel("측정소 수")

    # 막대 위에 값 표시
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f"{int(height)}", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    plt.savefig("04_pm10_grade_bar.png", dpi=150)
    plt.show()
    print("▶ '04_pm10_grade_bar.png' 저장 완료")

# ============================================================
# 4단계: 상관관계 분석
# ============================================================
print("\n" + "=" * 60)
print("4단계: 상관관계 분석")
print("=" * 60)

if len(numeric_cols) >= 2:
    # 상관계수 행렬 계산
    corr_matrix = df[numeric_cols].corr().round(2)
    print("\n▶ 상관계수 행렬:")
    print(corr_matrix)

    # 히트맵 시각화
    plt.figure(figsize=(10, 8))
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
    plt.savefig("05_correlation_heatmap.png", dpi=150)
    plt.show()
    print("▶ '05_correlation_heatmap.png' 저장 완료")

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
# 5단계: 인사이트 도출 (요약)
# ============================================================
print("\n" + "=" * 60)
print("5단계: EDA 인사이트 요약")
print("=" * 60)

print(f"""
[데이터 개요]
- 전체 데이터: {df.shape[0]}행 × {df.shape[1]}열
- 수치형 변수: {len(numeric_cols)}개
- 결측치가 있는 컬럼: {(df.isnull().sum() > 0).sum()}개

[발견한 내용]
- 결측치 현황을 확인하고, 전처리 방향을 결정할 수 있다
- 각 변수의 분포를 히스토그램과 박스플롯으로 확인했다
- 상관관계 분석을 통해 변수 간 관계를 파악했다

[다음 단계]
- 결측치 처리 (Part 2에서 배운 방법 적용)
- 필요한 특성 엔지니어링 수행
- 모델 학습 또는 대시보드 시각화로 연결
""")
