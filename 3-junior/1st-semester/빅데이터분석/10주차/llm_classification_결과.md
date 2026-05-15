# LLM HTTP 요청 분류 실험 결과 보고서

> **모델**: gemma3:1b (Ollama)  
> **데이터**: 100건 (정상 56건 / 공격 44건)

---

## 1. 기존 프롬프트 (영어)

### 프롬프트

```
You are a web security expert. Classify each HTTP request as "Normal" or "Anomalous" and provide a brief reason.

Examples:
Request: GET /index.jsp HTTP/1.1
Output: {"label": "Normal", "reason": "Standard page request, no suspicious pattern"}

Request: GET /search?q=' OR '1'='1 HTTP/1.1
Output: {"label": "Anomalous", "reason": "Classic SQL Injection pattern with OR 1=1"}

Now classify:
Request: {http_text}
Output:
```

### 결과

| 지표 | 값 |
|------|------|
| 정확도 (Accuracy) | **0.6800** |
| F1 Score | **0.6000** |
| 분류 실패 (Unknown) | 0건 |

```
              precision    recall  f1-score   support

      Normal       0.69      0.79      0.73        56
   Anomalous       0.67      0.55      0.60        44

    accuracy                           0.68       100
   macro avg       0.68      0.67      0.67       100
weighted avg       0.68      0.68      0.67       100
```

---

## 2. 기존 프롬프트 (한국어)

### 프롬프트

```
당신은 웹 보안 전문가입니다. 각 HTTP 요청을 "정상" 또는 "비정상"으로 분류하고 간단한 이유를 제시하세요.

예시:
요청: GET /index.jsp HTTP/1.1
출력: {"label": "정상", "reason": "표준 페이지 요청, 의심스러운 패턴 없음"}

요청: GET /search?q=' OR '1'='1 HTTP/1.1
출력: {"label": "비정상", "reason": "OR 1=1을 사용한 전형적인 SQL 인젝션 패턴"}

다음 요청을 분류하세요:
요청: {http_text}
출력:
```

### 결과

| 지표 | 값 |
|------|------|
| 정확도 (Accuracy) | **0.5600** |
| F1 Score | **0.0000** |
| 분류 실패 (Unknown) | 3건 |

```
              precision    recall  f1-score   support

      Normal       0.56      1.00      0.72        56
   Anomalous       0.00      0.00      0.00        44

    accuracy                           0.56       100
   macro avg       0.28      0.50      0.36       100
weighted avg       0.31      0.56      0.40       100
```

> ⚠️ **비고**: Anomalous recall이 0.00으로, 공격을 단 1건도 탐지하지 못함. gemma3:1b 모델이 한국어 레이블("정상"/"비정상")을 제대로 출력하지 못해 파싱 실패로 이어진 것으로 추정.

---

## 3. Claude로 gemma3:1b 모델용 최적화 프롬프트

### 프롬프트

```
You are an HTTP request classifier. Analyze requests and output JSON only.

RULES:
- Label is exactly "Normal" or "Anomalous"
- Reason is under 15 words
- Output only the JSON object, nothing else

ANOMALOUS patterns include:
- SQL Injection: OR 1=1, UNION SELECT, --, ' or "
- XSS: <script>, javascript:, onerror=
- Path Traversal: ../, ..\, /etc/passwd
- Command Injection: ;ls, |whoami, &&cmd
- Encoded attacks: %27, %3C, %00

Examples:
Request: GET /index.jsp HTTP/1.1
Output: {"label": "Normal", "reason": "Standard page request"}

Request: GET /search?q=' OR '1'='1 HTTP/1.1
Output: {"label": "Anomalous", "reason": "SQL injection OR 1=1 pattern"}

Request: GET /../../../etc/passwd HTTP/1.1
Output: {"label": "Anomalous", "reason": "Path traversal attack detected"}

Request: POST /login?user=<script>alert(1)</script> HTTP/1.1
Output: {"label": "Anomalous", "reason": "XSS script injection attempt"}

Classify this request:
Request: {http_text}
Output:
```

### 결과

| 지표 | 값 |
|------|------|
| 정확도 (Accuracy) | **0.6300** |
| F1 Score | **0.3934** |
| 분류 실패 (Unknown) | 3건 |

```
              precision    recall  f1-score   support

      Normal       0.61      0.91      0.73        56
   Anomalous       0.71      0.27      0.39        44

    accuracy                           0.63       100
   macro avg       0.66      0.59      0.56       100
weighted avg       0.65      0.63      0.58       100
```

---

## 4. 종합 비교

| 프롬프트 | 정확도 | F1 Score | Unknown | 비고 |
|----------|--------|----------|---------|------|
| 기존 (영어) | 0.6800 | 0.6000 | 0건 | **최고 성능** |
| 기존 (한국어) | 0.5600 | 0.0000 | 3건 | 공격 탐지 완전 실패 |
| Claude 최적화 (영어) | 0.6300 | 0.3934 | 3건 | Anomalous precision 향상, recall 저하 |

### 분석 요약

- **영어 프롬프트가 한국어보다 압도적으로 유리**: gemma3:1b는 소형 모델로 한국어 지시문 이해 및 한국어 레이블 출력에 취약함.
- **최적화 프롬프트의 트레이드오프**: 공격 패턴을 명시적으로 열거해 Anomalous precision(0.71)은 올랐으나, recall(0.27)이 크게 낮아져 탐지율이 오히려 저하됨.
- **기존 영어 프롬프트가 가장 균형적**: Anomalous F1(0.60)과 전체 정확도(0.68) 모두 가장 높음.
- **소형 LLM의 한계**: 1B 파라미터 모델은 복잡한 규칙 명시보다 단순하고 직관적인 few-shot 예시에 더 잘 반응하는 경향이 있음.
