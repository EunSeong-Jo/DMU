"""
실습 7: 3가지 분류 접근법 미리보기 (8주차 예고)
===============================================
통계(IQR) / 머신러닝(RandomForest) / LLM(Ollama)
3가지 방법을 CSIC 2010 데이터로 빠르게 맛보기 합니다.

실행: python approach_preview.py

* Ollama가 설치되어 있지 않아도 통계/ML 부분은 실행됩니다.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from urllib.parse import unquote
import pickle
import time
import os

print("=" * 65)
print("  [실습 7] 3가지 분류 접근법 미리보기")
print("=" * 65)

# 데이터 로드
pkl_path = os.path.join(os.path.dirname(__file__), "processed_data.pkl")
if not os.path.exists(pkl_path):
    print("\n  !! processed_data.pkl이 없습니다.")
    print("  >> 먼저 preprocessing.py와 feature_engineering.py를 실행하세요.")
    exit()

with open(pkl_path, "rb") as f:
    data = pickle.load(f)

X_train = data["X_train"]
X_test = data["X_test"]
y_train = data["y_train"]
y_test = data["y_test"]
feature_cols = data["feature_cols"]

# 미리보기용 소규모 샘플
SAMPLE_SIZE = 2000
np.random.seed(42)
test_idx = np.random.choice(len(X_test), min(SAMPLE_SIZE, len(X_test)), replace=False)
X_sample = X_test[test_idx]
y_sample = y_test[test_idx]

print(f"\n  학습 데이터: {X_train.shape[0]:,}건 (특성 {X_train.shape[1]}개)")
print(f"  테스트 샘플: {len(X_sample):,}건 (미리보기용)")


# ============================================================
# 접근법 1: 통계적 방법 (IQR 이상치 탐지)
# ============================================================
print(f"\n\n{'━' * 65}")
print("  접근법 1: 통계적 방법 (IQR 이상치 탐지)")
print(f"{'━' * 65}")

start_time = time.time()

# 각 특성에서 IQR 기반 이상치 판별
outlier_scores = np.zeros(len(X_sample))

for i in range(X_train.shape[1]):
    Q1 = np.percentile(X_train[:, i], 25)
    Q3 = np.percentile(X_train[:, i], 75)
    IQR = Q3 - Q1

    if IQR == 0:
        continue

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    is_outlier = (X_sample[:, i] < lower) | (X_sample[:, i] > upper)
    outlier_scores += is_outlier.astype(int)

# 이상치 점수가 임계값 이상이면 공격으로 판별
threshold = np.percentile(outlier_scores, 70)
iqr_pred = (outlier_scores >= max(threshold, 1)).astype(int)

iqr_time = time.time() - start_time
iqr_acc = accuracy_score(y_sample, iqr_pred)
iqr_f1 = f1_score(y_sample, iqr_pred, zero_division=0)

print(f"\n  방법: 추출된 {len(feature_cols)}개 특성에서 IQR 이상치 개수 합산")
print(f"  임계값: 이상치 점수 >= {max(threshold, 1):.0f}")
print(f"\n  결과:")
print(f"    정확도(Accuracy): {iqr_acc:.4f} ({iqr_acc*100:.1f}%)")
print(f"    F1-Score:         {iqr_f1:.4f}")
print(f"    소요 시간:        {iqr_time:.4f}초")

# 어떤 특성이 이상치 탐지에 기여했는지 확인
print(f"\n  특성별 이상치 비율 (공격 데이터):")
attack_mask = y_sample == 1
for i, col in enumerate(feature_cols):
    Q1 = np.percentile(X_train[:, i], 25)
    Q3 = np.percentile(X_train[:, i], 75)
    IQR = Q3 - Q1
    if IQR == 0:
        continue
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR
    outlier_ratio = ((X_sample[attack_mask, i] > upper) |
                     (X_sample[attack_mask, i] < lower)).mean()
    if outlier_ratio > 0.05:
        bar = "█" * int(outlier_ratio * 40)
        print(f"    {col:<25s} {outlier_ratio:>5.1%} {bar}")


# ============================================================
# 접근법 2: 머신러닝 (RandomForest)
# ============================================================
print(f"\n\n{'━' * 65}")
print("  접근법 2: 머신러닝 (RandomForest)")
print(f"{'━' * 65}")

print("\n  모델 학습 중...")
start_time = time.time()

rf_model = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)
train_time = time.time() - start_time

# 예측
start_time = time.time()
rf_pred = rf_model.predict(X_sample)
predict_time = time.time() - start_time

rf_acc = accuracy_score(y_sample, rf_pred)
rf_f1 = f1_score(y_sample, rf_pred, zero_division=0)

print(f"\n  결과:")
print(f"    정확도(Accuracy): {rf_acc:.4f} ({rf_acc*100:.1f}%)")
print(f"    F1-Score:         {rf_f1:.4f}")
print(f"    학습 시간:        {train_time:.2f}초")
print(f"    예측 시간:        {predict_time:.4f}초 ({len(X_sample)}건)")

# 특성 중요도 Top 10
print(f"\n  특성 중요도 Top 10:")
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1][:10]
for rank, idx in enumerate(indices, 1):
    bar = "█" * int(importances[idx] * 80)
    print(f"    {rank:2d}. {feature_cols[idx]:<25s} {importances[idx]:.4f} {bar}")

print(f"\n  >> 어떤 특성이 가장 중요한지 주목하세요!")
print(f"     우리가 직접 추출한 특성의 품질이 모델 성능을 결정합니다.")


# ============================================================
# 접근법 3: LLM (Ollama gemma3:4b) — HTTP 텍스트 직접 분류 ★
# ============================================================
print(f"\n\n{'━' * 65}")
print("  접근법 3: LLM (Ollama) — HTTP 요청 직접 분류 ★")
print(f"{'━' * 65}")

LLM_TEST_SIZE = 5

try:
    import ollama

    llm_sample_df = data["llm_sample"].head(LLM_TEST_SIZE)
    llm_correct = 0
    llm_total = 0
    start_time = time.time()

    print(f"\n  Ollama gemma3:4b로 {LLM_TEST_SIZE}건 HTTP 요청 분류 테스트...")
    print(f"  >> CSIC 2010의 장점: HTTP 텍스트를 그대로 LLM에 보여줄 수 있습니다!\n")

    for _, row in llm_sample_df.iterrows():
        true_label = "Anomalous" if row.get("is_attack", 0) == 1 else "Normal"
        true_label_alt = row.get("label", true_label)
        if true_label_alt in ["Normal", "Anomalous"]:
            true_label = true_label_alt

        # HTTP 요청 텍스트 구성
        method = row.get("method", "GET")
        url = str(row.get("url_decoded", row.get("url", "")))
        body = str(row.get("body_decoded", row.get("body", "")))
        if body == "nan":
            body = ""

        # URL 디코딩 시도
        try:
            url_display = unquote(url, encoding="latin-1")
        except Exception:
            url_display = url

        http_text = f"{method} {url_display} HTTP/1.1"
        if body:
            http_text += f"\nBody: {body[:200]}"

        prompt = f"""You are a web security expert. Analyze the following HTTP request and classify it as either "Normal" (legitimate) or "Anomalous" (attack/malicious).

HTTP Request:
{http_text}

Answer with ONLY one word: "Normal" or "Anomalous"."""

        response = ollama.chat(
            model="gemma3:4b",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response["message"]["content"].strip()

        if "normal" in answer.lower():
            predicted = "Normal"
        else:
            predicted = "Anomalous"

        is_correct = (predicted == true_label)
        llm_correct += int(is_correct)
        llm_total += 1
        mark = "O" if is_correct else "X"

        url_short = url_display[:60] + ("..." if len(url_display) > 60 else "")
        print(f"    [{mark}] 실제: {true_label:10s} | LLM: {predicted:10s} | "
              f"{method} {url_short}")

    llm_time = time.time() - start_time
    llm_acc = llm_correct / llm_total if llm_total > 0 else 0

    print(f"\n  결과 ({LLM_TEST_SIZE}건 기준):")
    print(f"    정확도: {llm_acc:.4f} ({llm_acc*100:.0f}%)")
    print(f"    소요 시간: {llm_time:.2f}초 (건당 {llm_time/LLM_TEST_SIZE:.2f}초)")
    print(f"    >> 1만 건이면 약 {llm_time/LLM_TEST_SIZE * 10000 / 60:.0f}분 소요 예상")
    print(f"\n  >> LLM은 HTTP 텍스트에서 공격 패턴을 사전 지식으로 판단합니다!")
    print(f"     CICIDS2017(숫자 데이터)보다 CSIC 2010(텍스트 데이터)에서 훨씬 효과적!")

except ImportError:
    print("\n  !! ollama 패키지가 설치되지 않았습니다.")
    print("  >> pip install ollama 로 설치하세요.")
    print("  >> 8주차에 본격적으로 실습합니다. 지금은 건너뛰어도 됩니다.")
    llm_acc = None
    llm_time = None

except Exception as e:
    print(f"\n  !! Ollama 연결 실패: {e}")
    print("  >> Ollama 서버가 실행 중인지 확인하세요.")
    print("  >> 8주차에 본격적으로 실습합니다.")
    llm_acc = None
    llm_time = None


# ============================================================
# 3가지 접근법 비교 요약
# ============================================================
print(f"\n\n{'━' * 65}")
print("  3가지 접근법 비교 요약")
print(f"{'━' * 65}")

print(f"\n  {'방법':<20s} | {'정확도':>8s} | {'F1-Score':>8s} | {'속도':>12s} | 특징")
print(f"  {'─' * 20}-+-{'─' * 8}-+-{'─' * 8}-+-{'─' * 12}-+-{'─' * 25}")
print(f"  {'통계 (IQR)':<20s} | {iqr_acc:>7.1%} | {iqr_f1:>8.4f} | {iqr_time:>10.4f}초 | 학습 불필요, 매우 빠름")
print(f"  {'머신러닝 (RF)':<20s} | {rf_acc:>7.1%} | {rf_f1:>8.4f} | {predict_time:>10.4f}초 | 높은 정확도, 특성 중요도")

if llm_acc is not None:
    print(f"  {'LLM (Ollama)':<20s} | {llm_acc:>7.1%} | {'N/A':>8s} | {llm_time:>10.2f}초 | HTTP 텍스트 직접 이해!")
else:
    print(f"  {'LLM (Ollama)':<20s} | {'미실행':>8s} | {'N/A':>8s} | {'N/A':>12s} | 8주차에 실습")

print(f"""
  핵심 관찰:
  1. 통계(IQR): 매우 빠르지만 정확도가 상대적으로 낮음
  2. 머신러닝(RF): 우리가 추출한 특성으로 높은 정확도 달성!
     → 특성 엔지니어링의 품질이 곧 모델 성능
  3. LLM: HTTP 텍스트를 그대로 이해 → CSIC 2010에 가장 적합한 방법
     → 건당 처리 시간이 길지만 판단 근거를 자연어로 설명 가능

  CSIC 2010 데이터셋의 장점:
  - 텍스트 데이터 → LLM이 공격 패턴을 사전 지식으로 판단 가능
  - 1교시 이론(SQL Injection, XSS 키워드)이 실제 데이터에서 보임
  - 특성 엔지니어링 과정을 직접 체험 (텍스트 → 숫자 변환)

  >> 8주차에서 더 정밀한 비교 실험을 진행합니다!
""")
print(f"{'━' * 65}")
