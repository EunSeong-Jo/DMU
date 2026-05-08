# 10주차 3교시 — Streamlit 웹 공격 탐지 대시보드 (자율 실습)

## 실습 코드 목록

| 실습 | 파일명 | 내용 | 실행 방법 |
|------|--------|------|----------|
| 실습 11 | `dashboard_starter.py` | 학생이 채울 스타터 코드 (TODO 마커 14개) | `streamlit run dashboard.py` |
| (제출용) | `dashboard.py` | 스타터를 복사한 뒤 학생이 완성하는 파일 | 동일 |

## 사전 준비 체크리스트

- [ ] 1교시 노트북 모두 실행 → `classification_results.pkl` 생성됨
- [ ] 2교시 노트북 모두 실행 (LLM 부분 동작 확인)
- [ ] Ollama 서버 실행 중 (`ollama serve`)
- [ ] 패키지 설치: `pip install streamlit plotly`

## 시작하기

```bash
# 1. 스타터를 dashboard.py로 복사
cd BigDataAnalysis/10_week
cp dashboard_starter.py dashboard.py

# 2. 일단 실행해보기 (TODO를 채우기 전에도 페이지는 뜸)
streamlit run dashboard.py
```

브라우저에서 `http://localhost:8501` 자동 열림.

## TODO 마커 위치 (총 14개)

| Step | TODO | 위치 | 난이도 | 예상 시간 |
|------|------|------|--------|----------|
| 1 | 1-A, 1-B | `load_models()` | ★ | 10분 |
| 2 | 2-A, 2-B | 입력 폼 (이미 작성됨, 확인만) | ★ | 5분 |
| 3 | 3-A ~ 3-E | `extract_features()` | ★★ | 25분 |
| 4 | 4-A ~ 4-E | 3가지 분류 함수 | ★★ | 25분 |
| 5 | 5-A ~ 5-C | 결과 카드 (이미 일부 작성됨) | ★ | 5분 |
| 6 | 6-A ~ 6-C | 비교 차트 (이미 일부 작성됨) | ★★ | 10분 |
| 7 | 7-A, 7-B | 사이드바 (이미 작성됨, 확장만) | ★ | 5분 |

> **합계**: 약 85분. 학생 페이스에 맞게 진행. 완성된 부분도 많아 핵심은 Step 3-4.

## 자율 실습 진행 가이드

### 가장 핵심: Step 3 — extract_features()
이 함수가 1교시 ML 모델의 입력을 만들어 줍니다. 7주차 [`preprocessing.py`](../7_week/preprocessing.py)의 특성 추출 로직을 함수로 옮기는 것이 가장 큰 작업입니다.

**힌트**: 7주차에서 만든 23개 특성을 모두 만들 필요 없이, **자주 등장하는 10~15개**만 만들고 나머지는 0으로 두어도 ML 모델은 동작합니다 (정확도는 약간 떨어짐).

### 도전 과제 (선택)

스타터의 마지막에 **다수결 최종 판정** 코드 주석이 있습니다. 주석을 풀고 활성화하면 4번째 카드로 표시됩니다.

추가 도전:
1. **키워드 하이라이트**: 입력 텍스트의 SQL/XSS 키워드를 `<span style='background:red'>`로 강조
2. **분류 이력**: `st.session_state.history`에 분류 결과 누적 → 표로 표시
3. **CSV 일괄 분류**: `st.file_uploader`로 CSV 업로드 → 모든 행을 RF로 분류 → CSV 다운로드 버튼

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `load_models() 함수의 TODO를 먼저 구현하세요` | Step 1 미완료 | TODO 1-A, 1-B 채우기 |
| 모든 모델이 항상 정상 판정 | `extract_features` 미구현(0벡터 반환) | TODO 3-A~3-E 채우기 |
| RF 신뢰도가 항상 0.5 | `classify_ml` 미구현 | TODO 4-C 채우기 |
| LLM 카드에 "Ollama 호출 미구현" | `classify_llm` 미구현 | TODO 4-D, 4-E 채우기 |
| `ConnectionError: ollama` | Ollama 서버 안 떠 있음 | 새 터미널에서 `ollama serve` |
| 페이지 변경 후 반영 안 됨 | Streamlit 캐시 | 브라우저 우상단 [⋮] → "Rerun" |
| 한글 깨짐 | 콘솔 인코딩 | Windows: `chcp 65001` 후 `streamlit run` |

## 제출 가이드

### 필수 제출물 (90분 내)
- `dashboard.py` (TODO 절반 이상 완성)
- 동작 스크린샷 1장 (3개 모델 결과가 보이는 화면)

### 우수 제출 (★)
- 모든 TODO 완성
- 도전 과제 1개 이상 구현
- 사이드바에 학번/이름 + 모델 정보 명시

### 평가 기준
- 30%: 입력 폼 + 모델 로드
- 40%: 3가지 분류 결과 표시 (IQR/RF/LLM 모두 동작)
- 20%: 비교 차트 그려짐
- 10%: 코드 정리 + 사이드바 + 도전 과제

## 시연 (수업 마지막 10분)

각자 만든 대시보드를 30초씩 화면 공유 시연:
- 어떤 입력을 넣었나
- 4가지 모델의 결과가 일치했는가, 달랐는가
- 가장 흥미로운 케이스 한 건 공유

> 학생들이 직접 만든 도구로 SQL Injection 등을 입력해 분류하면 1·2교시에서 배운 이론과 모델이 실제 사용 가능한 형태로 합쳐졌음을 체감하게 됩니다.
