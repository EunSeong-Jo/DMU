# 데이터 수집 실행 가이드

## 🚀 시작하기

### 1. 환경 준비

#### Python 버전 확인
```bash
python --version
# Python 3.8 이상 필요
```

#### 가상환경 생성 (권장)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 필수 패키지 설치
```bash
pip install -r requirements.txt
```

---

### 2. KOBIS API 키 발급

#### 2-1. 회원가입 및 로그인
1. [KOBIS 오픈API 사이트](https://www.kobis.or.kr/kobisopenapi/homepg/main/main.do) 접속
2. 회원가입 및 로그인

#### 2-2. API 키 발급
1. 상단 메뉴: `API 서비스` → `키 발급`
2. 이용약관 동의
3. 키 발급 완료 (즉시 발급됨)

#### 2-3. 환경변수 설정
```bash
# .env.example 파일을 복사하여 .env 파일 생성
cp .env.example .env

# .env 파일 편집 (메모장 또는 VS Code)
KOBIS_API_KEY=발급받은_API_키_입력
```

**예시:**
```
KOBIS_API_KEY=abc123def456ghi789
START_DATE=2019-01-01
END_DATE=2024-12-31
MAX_MOVIES=300
DELAY_SECONDS=2
MAX_RETRIES=3
```

---

### 3. 데이터 수집 실행

#### 3-1. KOBIS 데이터 수집 (1단계)

```bash
cd src
python kobis_collector.py
```

**예상 소요 시간**: 약 30분 ~ 1시간
**수집 결과**:
- `data/raw/kobis_boxoffice.csv` - 박스오피스 기본 정보
- `data/raw/kobis_movie_details.csv` - 영화 상세 정보
- `data/raw/kobis_merged.csv` - 병합된 최종 데이터

**실행 로그 예시:**
```
2024-11-05 10:00:00 - INFO - 박스오피스 수집 시작: 2019-01-01 ~ 2024-12-31
박스오피스 수집: 100%|████████████████| 312/312 [05:20<00:00]
2024-11-05 10:05:20 - INFO - 총 450편의 영화 수집 완료
2024-11-05 10:05:20 - INFO - 영화 상세정보 수집 시작: 300편
상세정보 수집: 100%|████████████████| 300/300 [15:00<00:00]
2024-11-05 10:20:20 - INFO - ✅ 데이터 수집 완료: 총 300편
```

#### 3-2. 네이버 데이터 수집 (2단계)

```bash
python naver_collector.py
```

**예상 소요 시간**: 약 2~3시간 (300편 × 50개 리뷰)
**수집 결과**:
- `data/raw/naver_ratings.csv` - 영화 평점 정보
- `data/raw/naver_reviews.csv` - 관객 리뷰 (15,000개)

**주의사항**:
- 처음 실행 시 ChromeDriver 자동 다운로드 (시간 소요)
- 네이버 크롤링 차단 방지를 위해 랜덤 대기 시간 적용
- 중간에 중단되면 이미 수집된 데이터는 저장됨

**실행 로그 예시:**
```
2024-11-05 11:00:00 - INFO - KOBIS 데이터 로드: 300편
2024-11-05 11:00:00 - INFO - Selenium 드라이버 초기화 완료
네이버 데이터 수집: 100%|████████████| 300/300 [2:15:30<00:00]
2024-11-05 13:15:30 - INFO - 평점 수집: 300편
2024-11-05 13:15:30 - INFO - 리뷰 수집: 15,000개
2024-11-05 13:15:30 - INFO - ✅ 네이버 데이터 수집 완료
```

---

## 🔧 트러블슈팅

### 문제 1: KOBIS API 키 오류
```
ERROR - KOBIS_API_KEY가 설정되지 않았습니다.
```

**해결책**:
1. `.env` 파일이 `src/` 폴더와 같은 경로에 있는지 확인
2. `.env` 파일에 `KOBIS_API_KEY=발급받은키` 형식으로 입력
3. 키 앞뒤 공백 제거

---

### 문제 2: ChromeDriver 오류
```
WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

**해결책**:
```bash
pip install --upgrade webdriver-manager
```

또는 수동 설치:
1. [ChromeDriver 다운로드](https://chromedriver.chromium.org/)
2. Chrome 버전과 일치하는 드라이버 다운로드
3. 시스템 PATH에 추가

---

### 문제 3: 네이버 크롤링 차단
```
WARNING - 영화 '{영화명}' 검색 결과 없음
```

**해결책**:
1. `naver_collector.py`의 `delay` 값을 증가 (2.0 → 3.0)
2. `headless=False`로 설정하여 브라우저 확인
3. User-Agent 변경

---

### 문제 4: 메모리 부족
```
MemoryError: Unable to allocate array
```

**해결책**:
1. 수집 대상 축소 (300편 → 100편)
2. `kobis_collector.py`의 `sample_interval` 증가 (7 → 14일)
3. 배치 처리로 분할 실행

---

## 📊 수집 데이터 확인

### Python으로 확인
```python
import pandas as pd

# KOBIS 데이터
kobis = pd.read_csv('data/raw/kobis_merged.csv')
print(f"KOBIS 데이터: {len(kobis)}편")
print(kobis.head())

# 네이버 평점
ratings = pd.read_csv('data/raw/naver_ratings.csv')
print(f"\n평점 데이터: {len(ratings)}편")
print(f"평균 네티즌 평점: {ratings['netizen_score'].mean():.2f}")

# 네이버 리뷰
reviews = pd.read_csv('data/raw/naver_reviews.csv')
print(f"\n리뷰 데이터: {len(reviews)}개")
print(reviews['score'].value_counts())
```

---

## ⏱️ 예상 일정

| 단계 | 작업 | 소요 시간 |
|------|------|-----------|
| 0 | 환경 설정 및 API 키 발급 | 30분 |
| 1 | KOBIS 데이터 수집 | 1시간 |
| 2 | 네이버 데이터 수집 | 2~3시간 |
| **총** | | **약 4시간** |

**권장 스케줄**:
- 1일차: 환경 설정 + KOBIS 수집
- 2일차: 네이버 수집 (장시간 소요)

---

## 💾 백업 및 버전관리

### 데이터 백업
```bash
# 수집 완료 후 백업
mkdir backup
cp -r data/raw backup/raw_$(date +%Y%m%d)
```

### Git 커밋
```bash
git add .
git commit -m "데이터 수집 완료: KOBIS 300편 + 네이버 리뷰 15,000개"
git push origin main
```

---

## 📞 도움말

### KOBIS API 문서
- [KOBIS Open API 가이드](https://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do)

### Selenium 문서
- [Selenium Python 문서](https://selenium-python.readthedocs.io/)

### 문의
- 과목: 빅데이터 응용프로그래밍
- 담당 교수: [교수명]
- 이메일: [이메일]
