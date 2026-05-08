# 2주차 실습 코드 요약

## 파일 목록 및 설명

### 1. Streamlit 웹 앱 (3개)

| 파일 | 주제 | 설명 |
|------|------|------|
| `app.py` | Streamlit 기초 | Streamlit 입문용 앱. 샘플 데이터프레임 표시, 막대 차트, 사이드바 텍스트 입력 등 기본 기능 소개 |
| `app_preprocessing.py` | 전처리 영향 분석 대시보드 | 가격-평점 샘플 데이터에서 결측치(중앙값 대체) + 이상치(IQR 제거) 전후의 상관계수 변화를 산점도로 비교 |
| `app_data_validator.py` | 데이터 품질 검증기 | CSV 파일을 업로드하면 선택한 두 수치형 컬럼에 대해 전처리 전/후 상관계수 변화, 산점도 비교, 데이터 정제 요약을 자동으로 보여주는 도구 |

### 2. Pandas 기초 및 데이터 분석 (2개)

| 파일 | 주제 | 설명 |
|------|------|------|
| `pandas_basics.py` | Pandas 기본 자료구조 | Series와 DataFrame 생성, 인덱스 접근, 통계 메서드(mean, sum, max), 조건 필터링 등 Pandas의 가장 기본적인 사용법 |
| `pandas_analysis.py` | 데이터 탐색-전처리-가공 전체 흐름 | 상품 데이터로 EDA 3단계 실습: (1) 탐색(shape, head, info, describe, value_counts), (2) 전처리(결측치 중앙값/평균 대체, 이상치 IQR 탐지), (3) 가공(필터링, 정렬, 그룹 집계, 특성 엔지니어링 — 매출액, 가격대, 평점등급 컬럼 생성) |

### 3. 데이터 전처리 실습 (3개)

| 파일 | 주제 | 설명 |
|------|------|------|
| `pandas_cleaning_practice.py` | 문자열 정제 & 타입 변환 | 현실적으로 지저분한 데이터(공백, 도시명 불일치, 쉼표 포함 숫자, 날짜 형식 혼재)를 4단계로 정제: strip/replace → to_numeric/to_datetime → 결측치 처리 → 중복 제거 |
| `pandas_encoding_practice.py` | 범주형 인코딩 | 변수 타입 판별(숫자이지만 범주형인 우편번호 등), 원-핫 인코딩(성별/지역), 레이블 인코딩(만족도 순서형), 최종 ML 입력 피처 구성까지의 흐름 |
| `pandas_merge_practice.py` | 데이터 결합 | concat(같은 구조 위아래 합치기)과 merge(공통 키로 결합 — inner/left join) 실습. 결합 후 groupby 집계까지의 실전 패턴 |

### 4. 분석 심화 (3개)

| 파일 | 주제 | 설명 |
|------|------|------|
| `preprocessing_impact.py` | 전처리가 상관계수에 미치는 영향 | 이상치/결측치가 포함된 가격-평점 데이터에서 전처리 전후 상관계수 변화를 계산하고, matplotlib/seaborn 산점도로 시각화하여 "GIGO → Clean" 효과를 보여줌 |
| `scaling_comparison.py` | 3가지 스케일링 비교 | MinMaxScaler, StandardScaler, RobustScaler를 동일 데이터에 적용하여 이상치가 있을 때 각 스케일러의 차이를 비교. RobustScaler가 이상치에 강건함을 증명. 올바른 train/test 분리 후 스케일링 순서(데이터 누수 방지)도 포함 |
| `performance_comparison.py` | 대용량 데이터 성능 비교 | 10만 행 데이터로 (1) for 루프 vs 벡터 연산, (2) apply vs np.where 속도 비교, (3) category 타입 메모리 절약, (4) 숫자 다운캐스팅 효과를 실측하여 대용량 처리 시 최적화 필요성을 보여줌 |

## 학습 흐름 (권장 순서)

```
pandas_basics.py          ← Pandas 기초 (Series, DataFrame)
    ↓
pandas_analysis.py        ← EDA 전체 흐름 (탐색 → 전처리 → 가공)
    ↓
pandas_cleaning_practice.py  ← 문자열 정제, 타입 변환
pandas_encoding_practice.py  ← 범주형 인코딩
pandas_merge_practice.py     ← 데이터 결합 (concat, merge)
    ↓
preprocessing_impact.py   ← 전처리가 분석 결과에 미치는 영향
scaling_comparison.py     ← 스케일링 방법 비교
    ↓
performance_comparison.py ← 대용량 데이터 최적화
    ↓
app.py                    ← Streamlit 기초
app_preprocessing.py      ← 전처리 영향 대시보드
app_data_validator.py     ← 데이터 품질 검증 도구
```

## 핵심 라이브러리

- **pandas**: 데이터 로드, 탐색, 전처리, 가공
- **numpy**: 벡터 연산, np.where, 랜덤 데이터 생성
- **matplotlib / seaborn**: 산점도, 회귀선 시각화
- **scikit-learn**: MinMaxScaler, StandardScaler, RobustScaler, train_test_split, LabelEncoder
- **streamlit**: 웹 대시보드, 데이터프레임 표시, 차트, 파일 업로드
