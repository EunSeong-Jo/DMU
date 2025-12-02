# ⚡ 빠른 시작 가이드

5분 안에 데이터 수집을 시작하세요!

## 📦 1단계: 설치 (2분)

```bash
# 1. 저장소 클론 (또는 이미 있으면 생략)
cd "C:\Users\asus\DMU\2-sophomore\2st-semester\빅데이터"

# 2. 가상환경 생성 및 활성화
cd korean-movie-analysis
python -m venv venv
venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt
```

## 🔑 2단계: API 키 설정 (1분)

```bash
# 1. .env 파일 생성
copy .env.example .env

# 2. 메모장으로 .env 파일 열기
notepad .env

# 3. KOBIS API 키 입력
KOBIS_API_KEY=여기에_발급받은_API_키_입력
```

### KOBIS API 키 발급 방법
1. https://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do
2. 회원가입 → 로그인
3. `키 발급` 클릭 (즉시 발급)

## 🧪 3단계: 테스트 실행 (1분)

```bash
cd src
python test_collection.py
```

선택: `1` (KOBIS API 테스트)

**성공 시 출력:**
```
✅ KOBIS API 테스트 통과!
```

## 🚀 4단계: 본격 데이터 수집 (1분 설정)

### KOBIS 데이터 수집
```bash
python kobis_collector.py
```
⏱️ 예상 시간: 30분~1시간

### 네이버 데이터 수집
```bash
python naver_collector.py
```
⏱️ 예상 시간: 2~3시간

---

## ✅ 체크리스트

- [ ] Python 3.8+ 설치됨
- [ ] 패키지 설치 완료 (`pip install -r requirements.txt`)
- [ ] .env 파일에 KOBIS_API_KEY 설정
- [ ] 테스트 실행 성공
- [ ] KOBIS 데이터 수집 시작
- [ ] 네이버 데이터 수집 시작

---

## 🆘 문제 발생 시

### KOBIS API 오류
```bash
# API 키 확인
type .env
```
→ `KOBIS_API_KEY=` 뒤에 키가 있는지 확인

### Selenium 오류
```bash
# ChromeDriver 재설치
pip install --upgrade webdriver-manager
```

### 자세한 가이드
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 상세 설정 가이드
- [README.md](README.md) - 프로젝트 개요

---

## 📊 수집 완료 후

```python
# 데이터 확인
import pandas as pd

kobis = pd.read_csv('../data/raw/kobis_merged.csv')
print(f"수집된 영화: {len(kobis)}편")

naver = pd.read_csv('../data/raw/naver_reviews.csv')
print(f"수집된 리뷰: {len(naver)}개")
```

**다음 단계**: 데이터 전처리 및 분석 시작! 🎉
