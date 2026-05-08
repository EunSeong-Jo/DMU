# 10주차 1교시 — 통계 + 머신러닝 분류

## 실습 코드 목록

| 실습 | 파일명 | 내용 | 실행 방법 |
|------|--------|------|----------|
| 실습 8 | `ml_classification.ipynb` | IQR + RandomForest + XGBoost 학습/평가 | JupyterLab에서 더블클릭 |

## 사전 준비

1. **7주차 산출물 확인**: `../7_week/processed_data.pkl`이 있어야 합니다.
   - 없다면: `cd ../7_week && python feature_engineering.py` 실행

2. **패키지 설치**:
   ```bash
   pip install scikit-learn xgboost plotly
   ```

3. **JupyterLab 실행**:
   ```bash
   jupyter lab
   ```
   브라우저에서 `BigDataAnalysis/10_week/ml_classification.ipynb` 더블클릭

## 실습 흐름 (1교시 90분)

### Step 1 — 데이터 로드 (5분)
- 셀 [Setup]: 7주차 `processed_data.pkl` 로드 → X_train/X_test/y_train/y_test 확인

### Step 2 — IQR 이상치 탐지 (15분)
- 셀 [1]: 23개 특성에서 IQR 경계 계산 + 점수 합산
- 셀 [2]: 정상/공격 점수 분포 히스토그램
- **관찰 포인트**: 공격 데이터의 점수가 임계값(2) 위에 분포하는가?

### Step 3 — RandomForest (20분)
- 셀 [3]: 100개 트리 학습 + 예측 + classification_report
- 셀 [4]: 특성 중요도 Top 10
- **관찰 포인트**: 어떤 특성이 분류에 가장 기여하는가?

### Step 4 — XGBoost (10분)
- 셀 [5]: Gradient Boosting 학습 + 평가
- **관찰 포인트**: RF와 정확도/속도 차이?

### Step 5 — 평가 지표 (15분)
- 셀 [6]: 혼동행렬 → TP/FP/FN/TN 해석
- 셀 [7]: ROC Curve + AUC
- **★ 핵심**: 보안에서는 정확도보다 **재현율(Recall)** 이 중요!

### Step 6 — 비교 + 저장 (5분)
- 셀 [8]: 세 방법 비교 표 → `classification_results.pkl` 저장 (2교시에서 사용)

## 생성 파일

| 파일 | 생성 시점 | 용도 |
|------|----------|------|
| `classification_results.pkl` | 셀 [8] | 2교시 LLM 비교 + 3교시 대시보드 |

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `FileNotFoundError: ../7_week/processed_data.pkl` | 7주차 미실행 | `cd ../7_week && python feature_engineering.py` |
| `ModuleNotFoundError: xgboost` | 패키지 미설치 | `pip install xgboost` |
| 학습 시간이 너무 오래 걸림 | 데이터 큼 | `n_estimators=50`으로 줄여 빠른 시연 가능 |

## 관찰 포인트 — 학생들에게 던질 질문

1. **IQR 정확도가 RF보다 낮은 이유는?** → IQR은 특성 간 상호작용을 무시
2. **특성 중요도 1위는 무엇인가?** → 7주차에서 만든 어떤 특성이 가장 효과적이었나
3. **F1과 정확도 중 무엇을 봐야 하는가?** → 불균형 데이터에서는 F1 + Recall
4. **혼동행렬에서 FN을 줄이려면?** → 임계값 조정, 또는 class_weight 조정
