# 10주차 2교시 — Ollama LLM 분류 + 3가지 방법 비교

## 실습 코드 목록

| 실습 | 파일명 | 내용 | 실행 방법 |
|------|--------|------|----------|
| 실습 9 | `llm_classification.ipynb` | Ollama로 100건 HTTP 요청 분류 + 평가 | JupyterLab에서 더블클릭 |
| 실습 10 | `comparison_analysis.ipynb` | 3가지 방법 종합 비교 차트 | JupyterLab에서 더블클릭 |

## 사전 준비

1. **1교시 산출물 확인**: `classification_results.pkl`이 있어야 합니다.
   - 없다면: `ml_classification.ipynb`의 셀 [8] 실행

2. **Ollama 설치 확인**:
   ```bash
   ollama list                    # gemma3:4b가 보여야 함
   ```
   - 없다면: `ollama pull gemma3:4b` (약 3GB, 5~10분 소요)

3. **Ollama 서버 실행**:
   ```bash
   ollama serve                   # 별도 터미널에서 실행 유지
   ```

4. **패키지 설치**:
   ```bash
   pip install ollama
   ```

## 실습 흐름 (2교시 90분)

### Part A — `llm_classification.ipynb` (60분)

#### Step 1 — 셋업 (5분)
- 셀 [Setup]: LLM용 100건 샘플 로드

#### Step 2 — 프롬프트 설계 (15분)
- 셀 [1]: Few-shot + JSON 형식 프롬프트 작성
- 단건 테스트로 응답 형태 확인
- **관찰 포인트**: 예시 없이 답하게 하면 어떻게 되는가? (실험)

#### Step 3 — 100건 분류 (30분 — 대부분 LLM 추론 시간)
- 셀 [2]: 100건 분류 실행 (CPU 기준 2~5분)
- **그동안 강사**: 다른 학생 화면 점검, 프롬프트 변형 토론

#### Step 4 — 평가 (5분)
- 셀 [3]: 정확도 + F1 + classification_report

#### Step 5 — 자연어 근거 검토 (5분) ★
- 셀 [4]: LLM이 공격으로 판정한 사례의 reason 출력
- **관찰 포인트**: ML 모델은 절대 못 하는 것 — 자연어 설명!

#### Step 6 — 결과 저장 (선택, ~1분)
- 셀 [5]: `llm_classification_results.pkl` 생성

### Part B — `comparison_analysis.ipynb` (30분)

- 셀 [1]: 4가지 방법 통합 표 (IQR/RF/XGB/LLM)
- 셀 [2]: 정확도/F1 막대 차트
- 셀 [3]: 정확도 vs 속도 산점도 (X축 로그)
- **★ 핵심 토론**: 어떤 방법이 "최고"인가? → 정답은 "시나리오에 따라 다름"

## 생성 파일

| 파일 | 생성 시점 | 용도 |
|------|----------|------|
| `llm_classification_results.pkl` | `llm_classification.ipynb` 셀 [5] | 종합 비교에 사용 |

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `ConnectionError` | Ollama 서버 미실행 | 새 터미널에서 `ollama serve` |
| `Model not found: gemma3:4b` | 모델 미다운로드 | `ollama pull gemma3:4b` |
| LLM이 매번 다른 답 | 비결정성 (정상) | `options={"temperature": 0}` 추가 |
| LLM이 영어로 답하기 거부 | 한국어 시스템 프롬프트 영향 | 프롬프트를 영어로 통일 |
| 100건이 너무 오래 걸림 | CPU 환경 | `llm_sample.head(20)`으로 줄이기 (시연용) |
| 정확도가 너무 낮음 | 프롬프트가 부적절 | Few-shot 예시 추가, JSON 형식 강제 |

## 관찰 포인트 — 학생들에게 던질 질문

1. **LLM의 오탐(FP) 사례를 보세요. 왜 정상을 공격으로 오인했나요?** → 키워드 매칭의 한계
2. **LLM의 미탐(FN) 사례는?** → 잘 알려지지 않은 패턴 또는 인코딩된 공격
3. **자연어 근거가 ML보다 어떤 점에서 더 유용한가?** → 보안 분석가 검토 보조
4. **LLM을 실시간 트래픽에 쓸 수 있을까?** → 처리 속도 제약 → 하이브리드 필요
5. **프롬프트만 바꿔서 정확도를 더 올릴 수 있을까?** → 도전 과제
