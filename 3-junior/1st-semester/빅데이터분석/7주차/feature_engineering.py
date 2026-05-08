"""
실습 6: 특성 엔지니어링 + 학습 데이터 준비
==========================================
추출된 숫자형 특성을 스케일링하고, 학습/테스트 데이터를 분할합니다.
8주차 모델 학습에 바로 사용할 수 있는 데이터를 저장합니다.

실행: python feature_engineering.py
(preprocessing.py를 먼저 실행해야 합니다)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import os

print("=" * 65)
print("  [실습 6] 특성 엔지니어링 + 학습 데이터 준비")
print("=" * 65)

# 전처리된 데이터 로드
data_path = os.path.join(os.path.dirname(__file__), "csic2010_cleaned.csv")
if not os.path.exists(data_path):
    print(f"\n  !! csic2010_cleaned.csv 파일이 없습니다.")
    print(f"  >> 먼저 preprocessing.py를 실행하세요.")
    exit()

df = pd.read_csv(data_path)
print(f"\n  데이터 로드: {df.shape[0]:,}행 x {df.shape[1]}열")


# ============================================================
# Step 1: 라벨 인코딩
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 1: 라벨 인코딩")
print(f"{'─' * 65}")

# 이진 분류 라벨 (Normal=0, Anomalous=1)
df["is_attack"] = (df["label"] == "Anomalous").astype(int)

normal_count = (df["is_attack"] == 0).sum()
attack_count = (df["is_attack"] == 1).sum()

print(f"\n  정상 (Normal=0):    {normal_count:>8,}건 ({normal_count/len(df)*100:.1f}%)")
print(f"  공격 (Anomalous=1): {attack_count:>8,}건 ({attack_count/len(df)*100:.1f}%)")


# ============================================================
# Step 2: 특성(Feature) 선택
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 2: 특성 선택")
print(f"{'─' * 65}")

# preprocessing.py에서 추출한 숫자형 특성
feature_cols = [
    # 길이 관련
    "url_length", "body_length", "total_length",
    # URL 구조
    "num_params", "path_depth", "has_query", "query_length", "body_num_params",
    # 공격 키워드
    "has_sql", "sql_keyword_count", "has_xss",
    "has_traversal", "traversal_count",
    "has_cmd_injection", "has_crlf",
    # 특수문자 / 공백
    "num_special_chars", "special_char_ratio",
    "num_dots", "num_slashes", "num_spaces",
    # 통계
    "url_entropy", "digit_ratio", "upper_ratio",
]

# 존재하지 않는 컬럼 제외
available_cols = [c for c in feature_cols if c in df.columns]
missing_cols = [c for c in feature_cols if c not in df.columns]

if missing_cols:
    print(f"\n  !! 누락된 특성: {missing_cols}")
    print(f"  >> preprocessing.py를 다시 실행하세요.")

feature_cols = available_cols

print(f"\n  사용할 특성: {len(feature_cols)}개")
print(f"  특성 목록:")
for i, col in enumerate(feature_cols, 1):
    mean_val = df[col].mean()
    print(f"    {i:2d}. {col:<25s}  (평균: {mean_val:.3f})")


# ============================================================
# Step 3: 결측치 처리 (숫자형 특성)
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 3: 결측치 처리")
print(f"{'─' * 65}")

missing = df[feature_cols].isnull().sum()
missing_total = missing.sum()
print(f"\n  결측치 총 개수: {missing_total}")

if missing_total > 0:
    for col in feature_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"    {col}: 중앙값({median_val:.2f})으로 대체")
    print(f"  처리 후 결측치: {df[feature_cols].isnull().sum().sum()}")
else:
    print("  결측치 없음!")


# ============================================================
# Step 4: 학습/테스트 데이터 분할 (80:20)
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 4: 학습/테스트 데이터 분할 (80:20)")
print(f"{'─' * 65}")

X = df[feature_cols].values
y = df["is_attack"].values

# stratify: 정상/공격 비율을 학습/테스트에 동일하게 유지
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n  학습 데이터: {X_train.shape[0]:,}건")
print(f"  테스트 데이터: {X_test.shape[0]:,}건")
print(f"  학습 공격 비율: {y_train.mean()*100:.1f}%")
print(f"  테스트 공격 비율: {y_test.mean()*100:.1f}%")
print(f"  >> stratify 덕분에 비율이 동일합니다!")


# ============================================================
# Step 5: 특성 스케일링 (StandardScaler)
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 5: 특성 스케일링 (StandardScaler)")
print(f"{'─' * 65}")

scaler = StandardScaler()

# ★ 핵심: 학습 데이터로 fit, 테스트 데이터는 transform만!
X_train_scaled = scaler.fit_transform(X_train)   # fit + transform
X_test_scaled = scaler.transform(X_test)          # transform만

print(f"\n  스케일링 전 (url_length):")
url_idx = feature_cols.index("url_length")
print(f"    학습 평균: {X_train[:, url_idx].mean():.2f}, "
      f"표준편차: {X_train[:, url_idx].std():.2f}")
print(f"\n  스케일링 후:")
print(f"    학습 평균: {X_train_scaled[:, url_idx].mean():.4f}, "
      f"표준편차: {X_train_scaled[:, url_idx].std():.4f}")

print(f"\n  >> 왜 따로 할까?")
print(f"     테스트 데이터 = '미래의 새로운 HTTP 요청'")
print(f"     미래 데이터의 통계를 미리 알 수 없으므로,")
print(f"     학습 데이터의 통계로만 변환 = 데이터 누수(Data Leakage) 방지!")


# ============================================================
# Step 6: 클래스 불균형 확인
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 6: 클래스 불균형 확인")
print(f"{'─' * 65}")

normal_train = (y_train == 0).sum()
attack_train = (y_train == 1).sum()
ratio = normal_train / attack_train

print(f"\n  학습 데이터:")
normal_bar = "█" * int(normal_train / len(y_train) * 40)
attack_bar = "█" * int(attack_train / len(y_train) * 40)
print(f"    정상:  {normal_train:>8,}건 {normal_bar}")
print(f"    공격:  {attack_train:>8,}건 {attack_bar}")
print(f"\n  정상:공격 비율 = {ratio:.1f}:1")
print(f"  >> class_weight='balanced' 옵션으로 8주차에 대응합니다")


# ============================================================
# Step 7: 8주차용 데이터 저장 (pickle)
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 7: 8주차용 데이터 저장")
print(f"{'─' * 65}")

# LLM 테스트용 샘플 (원본 텍스트 포함 — LLM에 HTTP 요청을 보여줄 때 사용)
text_cols = ["method", "url", "url_decoded", "body", "body_decoded",
             "full_text", "label"]
available_text_cols = [c for c in text_cols if c in df.columns]
llm_sample = df[available_text_cols + feature_cols + ["is_attack"]].sample(
    500, random_state=42
)

processed_data = {
    "X_train": X_train_scaled,
    "X_test": X_test_scaled,
    "X_train_raw": X_train,
    "X_test_raw": X_test,
    "y_train": y_train,
    "y_test": y_test,
    "feature_cols": feature_cols,
    "scaler": scaler,
    "llm_sample": llm_sample,
}

output_path = os.path.join(os.path.dirname(__file__), "processed_data.pkl")
with open(output_path, "wb") as f:
    pickle.dump(processed_data, f)

print(f"\n  저장 완료: processed_data.pkl")
print(f"    학습 데이터: {X_train_scaled.shape}")
print(f"    테스트 데이터: {X_test_scaled.shape}")
print(f"    특성 수: {len(feature_cols)}개")
print(f"    LLM 테스트 샘플: {len(llm_sample)}건 (원본 텍스트 포함)")


# ============================================================
# 전체 요약
# ============================================================
print(f"\n{'=' * 65}")
print("  7주차 전체 작업 요약")
print(f"{'=' * 65}")

print("""
  1교시: 웹 보안 이론 + 공격 유형 체험
    -> attack_examples.py, attack_quiz.py

  2교시: CSIC 2010 데이터 로드 + EDA + 시각화
    -> data_load_explore.ipynb, eda_keyword_analysis.ipynb, eda_visualization.ipynb / eda_visualization.py (Streamlit)

  3교시: 전처리 + 특성 엔지니어링 + 학습 데이터 준비
    -> preprocessing.py, feature_engineering.py (지금 이 파일)

  생성된 데이터 파일:
    - csic2010_requests.csv    (파싱된 HTTP 요청 데이터)
    - csic2010_cleaned.csv     (전처리 + 특성 추출 완료)
    - processed_data.pkl       (8주차 모델 학습용)
""")

print("  >> 8주차에서 processed_data.pkl을 로드하여")
print("     통계/ML/LLM 3가지 방법으로 분류 비교 실험을 합니다!")
print(f"{'=' * 65}")
