# 프로젝트 진행 상황 요약

**작성일**: 2024-11-05
**작성자**: 조은성 (20232678)
**과목**: 빅데이터응용프로그래밍
**단계**: 기말고사 준비 - 데이터 수집 단계

---

## 📌 프로젝트 개요

### 주제
**"데이터 기반 한국영화 성공 공식 분석"**

### 연구 목표
1. 한국 영화의 흥행 성공을 결정짓는 주요 요인 파악
2. 계절별/장르별 개봉 전략이 흥행에 미치는 영향 분석
3. 관객 리뷰 감성과 실제 흥행 성과 간 상관관계 규명
4. 머신러닝 기반 흥행 예측 모델 구축

### 검증 가설
- **H1**: 여름/겨울 성수기 개봉 영화가 봄/가을보다 평균 관객수 30% 이상 높다
- **H2**: 액션/SF 장르가 드라마/멜로보다 흥행 성공률 2배 높다
- **H3**: 네이버 평점 8.0 이상 영화는 7.0 이하 대비 흥행 성공률 5배 높다
- **H4**: 긍정 리뷰 비율 70% 이상 영화는 흥행 성공 확률 80% 이상이다

---

## 📊 중간고사 vs 기말고사 변경사항

### 중간고사 계획
- 데이터 출처: KOBIS + 네이버 + Kaggle 해외 데이터
- 목표: 300편 영화 + 리뷰 (개수 미정)
- 분석: Random Forest

### 기말고사 수정 계획 (현재)
| 항목 | 중간고사 | 기말고사 (수정) | 변경 이유 |
|------|----------|----------------|-----------|
| **데이터 출처** | KOBIS + 네이버 + Kaggle | KOBIS + 네이버 | 시간 제약, 집중도 향상 |
| **영화 수** | 불명확 | 300편 (명확) | 현실적 목표 설정 |
| **리뷰 수** | 100개 샘플 | 영화당 50개 (총 15,000개) | 통계적 유의성 확보 |
| **분석 기간** | 2019-2024 | 2019-2024 (동일) | - |
| **성공 기준** | 미정 | 관객수 300만 이상 | 명확한 기준 설정 |
| **모델** | Random Forest | RF + Logistic Regression | 해석력 향상 |

---

## 🗂️ 프로젝트 구조

```
korean-movie-analysis/
│
├── README.md                    # 프로젝트 전체 개요
├── PROJECT_SUMMARY.md           # 현재 진행상황 요약 (이 파일)
├── QUICKSTART.md                # 5분 빠른 시작 가이드
├── SETUP_GUIDE.md               # 상세 설정 및 실행 가이드
├── requirements.txt             # Python 패키지 목록
├── .env.example                 # 환경변수 템플릿
├── .gitignore                   # Git 제외 파일
│
├── data/                        # 데이터 저장소
│   ├── raw/                     # 원본 데이터 (수집 직후)
│   │   ├── kobis_boxoffice.csv
│   │   ├── kobis_movie_details.csv
│   │   ├── kobis_merged.csv     # KOBIS 최종 통합
│   │   ├── naver_ratings.csv
│   │   └── naver_reviews.csv    # 네이버 리뷰
│   ├── processed/               # 전처리 데이터
│   ├── final/                   # 최종 분석 데이터
│   └── test/                    # 테스트 데이터
│
├── src/                         # 소스 코드
│   ├── kobis_collector.py       # KOBIS API 데이터 수집기 ✅
│   ├── naver_collector.py       # 네이버 크롤러 ✅
│   ├── test_collection.py       # 테스트 스크립트 ✅
│   ├── preprocessing.py         # (예정) 데이터 전처리
│   └── analysis.py              # (예정) 분석 및 모델링
│
├── notebooks/                   # Jupyter Notebooks
│   ├── 01_data_collection.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_EDA.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_machine_learning.ipynb
│
├── visualizations/              # 시각화 결과
│   ├── eda/
│   ├── statistical/
│   └── ml/
│
├── models/                      # 학습된 모델
│   ├── random_forest.pkl
│   └── logistic_regression.pkl
│
└── reports/                     # 보고서
    ├── midterm_plan.pdf         # 중간고사 계획서
    ├── final_report.pdf         # (예정) 기말고사 보고서
    └── presentation.pptx        # (예정) 발표 자료
```

---

## ✅ 완료된 작업 (1주차)

### 1. 프로젝트 초기 설정
- [x] 프로젝트 폴더 구조 생성
- [x] README.md 작성
- [x] requirements.txt 패키지 목록 작성
- [x] .gitignore 설정
- [x] 환경변수 템플릿 (.env.example) 작성

### 2. 데이터 수집 코드 작성
- [x] **kobis_collector.py** 완성
  - KOBIS API 연동
  - 일별 박스오피스 조회
  - 영화 상세정보 조회
  - 자동 데이터 병합
  - 에러 핸들링 및 로깅

- [x] **naver_collector.py** 완성
  - 영화 제목으로 네이버 코드 검색
  - 영화 평점 정보 수집
  - 관객 리뷰 수집 (Selenium)
  - 크롤링 방지 대응 (랜덤 delay)
  - ChromeDriver 자동 관리

- [x] **test_collection.py** 완성
  - KOBIS API 연결 테스트
  - 네이버 크롤러 테스트
  - 수집 데이터 검증
  - 소규모 테스트 기능

### 3. 문서화
- [x] QUICKSTART.md - 빠른 시작 가이드
- [x] SETUP_GUIDE.md - 상세 설정 가이드
- [x] PROJECT_SUMMARY.md - 진행상황 요약 (이 파일)

---

## 🚧 진행 중인 작업 (현재 단계)

### 현재 위치: **데이터 수집 준비 완료**

다음 단계로 넘어가기 전에 해야 할 일:

1. **환경 설정** (5분)
   ```bash
   cd "C:\Users\asus\DMU\2-sophomore\2st-semester\빅데이터\korean-movie-analysis"
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **KOBIS API 키 발급** (3분)
   - https://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do
   - 회원가입 → 로그인 → 키 발급

3. **.env 파일 설정** (1분)
   ```bash
   copy .env.example .env
   notepad .env
   ```

   `.env` 파일 내용:
   ```
   KOBIS_API_KEY=발급받은_API_키_입력
   START_DATE=2019-01-01
   END_DATE=2024-12-31
   MAX_MOVIES=300
   DELAY_SECONDS=2
   MAX_RETRIES=3
   ```

4. **테스트 실행** (2분)
   ```bash
   cd src
   python test_collection.py
   # 선택: 1 (KOBIS API 테스트)
   ```

5. **본격 수집 시작**
   ```bash
   # KOBIS 데이터 수집 (30분~1시간)
   python kobis_collector.py

   # 네이버 데이터 수집 (2~3시간)
   python naver_collector.py
   ```

---

## 📅 전체 일정 (5주 계획)

| 주차 | 작업 | 상태 | 예상 시간 |
|------|------|------|-----------|
| **1주차** | **데이터 수집** | ✅ 코드 완료, ⏳ 실행 대기 | 15시간 |
| | KOBIS API 연동 및 데이터 수집 | ✅ 완료 | 5시간 |
| | 영화 상세정보 수집 | ✅ 완료 | 8시간 |
| | 네이버 크롤링 환경 구축 | ✅ 완료 | 2시간 |
| **2주차** | **데이터 전처리** | ⏳ 예정 | 18시간 |
| | 네이버 평점/리뷰 수집 | ⏳ 대기 | 10시간 |
| | 데이터 통합 및 전처리 | 📝 계획 | 3시간 |
| | 파생변수 생성 | 📝 계획 | 2시간 |
| | 텍스트 전처리 (감성분석) | 📝 계획 | 3시간 |
| **3주차** | **EDA + 통계분석** | 📝 계획 | 15시간 |
| | 기술통계 및 시각화 | 📝 계획 | 5시간 |
| | 가설 검증 (T-test, 카이제곱) | 📝 계획 | 4시간 |
| | 상관분석 및 다변량 분석 | 📝 계획 | 3시간 |
| | 텍스트 분석 (리뷰 키워드) | 📝 계획 | 3시간 |
| **4주차** | **머신러닝 모델링** | 📝 계획 | 15시간 |
| | Random Forest 모델 구축 | 📝 계획 | 5시간 |
| | Logistic Regression 구축 | 📝 계획 | 3시간 |
| | 모델 평가 및 비교 | 📝 계획 | 3시간 |
| | Feature Importance 분석 | 📝 계획 | 4시간 |
| **5주차** | **결과 정리 + 보고서** | 📝 계획 | 17시간 |
| | 핵심 인사이트 도출 | 📝 계획 | 4시간 |
| | 시각화 자료 정리 (15개) | 📝 계획 | 3시간 |
| | 최종 보고서 작성 | 📝 계획 | 6시간 |
| | PPT 제작 | 📝 계획 | 4시간 |

**총 예상 시간**: 80시간 (주당 16시간)

---

## 🎯 수집 목표 데이터

### KOBIS API 데이터
| 데이터 | 목표 | 주요 변수 |
|--------|------|-----------|
| 영화 수 | 300편 | movieCd, movieNm |
| 기본 정보 | 300편 | openDt, genres, directors, actors |
| 흥행 정보 | 300편 | audiAcc, salesAcc, screens |
| 기간 | 2019-2024 | prdtYear |

### 네이버 데이터
| 데이터 | 목표 | 주요 변수 |
|--------|------|-----------|
| 영화 평점 | 300편 | netizen_score, critic_score |
| 관객 리뷰 | 15,000개 | review_text, score, date |
| 영화당 리뷰 | 50개 | sympathy (공감수) |

---

## 📊 데이터 전처리 계획 (2주차)

### 1. 결측치 처리
```python
preprocessing_plan = {
    "누적관객수": "필수값 - 결측 시 제거",
    "네이버평점": "중앙값 대체",
    "감독/배우": "'정보없음'으로 대체",
    "장르": "'기타'로 분류"
}
```

### 2. 이상치 처리
- IQR 방식 이상치 탐지 및 제거
- 대상 변수: 누적관객수, 스크린수, 상영횟수

### 3. 파생변수 생성
```python
derived_variables = {
    "개봉_계절": "봄(3-5)/여름(6-8)/가을(9-11)/겨울(12-2)",
    "흥행_성공": "관객수 >= 300만 (1) else (0)",
    "흥행_등급": "대박(1000만+)/히트(500만+)/중박(300만+)/실패",
    "스크린당_관객": "누적관객수 / 최대스크린수",
    "긍정비율": "평점 8점 이상 리뷰 비율",
    "감성점수": "KoNLPy 기반 감성사전 점수"
}
```

### 4. 텍스트 전처리 (리뷰)
- 특수문자 제거
- 형태소 분석 (KoNLPy Okt)
- 불용어 제거
- 감성 사전 기반 점수화

---

## 📈 분석 방법론 (3-4주차)

### Phase 1: 탐색적 데이터 분석 (EDA)
1. 기술통계량 계산
2. 시각화 (15개)
   - 연도별 흥행 추이
   - 장르별 성과
   - 개봉 시기 히트맵
   - 평점-관객수 상관관계
   - 워드클라우드 등
3. 박스오피스 수익 분포 분석

### Phase 2: 통계 검정
1. **H1 검증**: T-test (계절별 관객수)
2. **H2 검증**: 카이제곱 검정 (장르별 성공률)
3. **H3 검증**: Logistic Regression (평점과 성공)
4. **H4 검증**: 상관분석 (감성과 흥행)

### Phase 3: 머신러닝 모델링
1. **Random Forest**
   - 흥행 성공 예측 (분류)
   - Feature Importance 분석
   - 교차검증 (5-fold)

2. **Logistic Regression**
   - 해석 가능한 계수
   - Odds Ratio 계산
   - 확률 예측

3. **모델 평가**
   - Accuracy, Precision, Recall
   - ROC-AUC Score
   - Confusion Matrix

---

## 🎓 기말고사 보고서 구성안

### 목차 (가이드 준수)
1. **표지 및 요약**
   - 과목명/학번/이름/제출일
   - 프로젝트 요약 (300자)

2. **주제 및 목적 재정리**
   - 중간고사 대비 변경사항
   - 최종 연구 목표 및 가설

3. **데이터 수집 및 전처리**
   - 수집 데이터 개요 (KOBIS 300편 + 네이버 15,000개 리뷰)
   - 수집 과정 (스크린샷 포함)
   - 전처리 과정 (Before/After)

4. **분석 과정**
   - 탐색적 데이터 분석 (10개 시각화)
   - 통계 검정 (H1-H4 검증)
   - 머신러닝 모델링 (RF + LR)

5. **주요 결과 및 해석**
   - 핵심 인사이트 5개
   - 가설 검증 결과
   - Feature Importance

6. **결론 및 한계**
   - 연구 의의
   - 실무 활용 방안
   - 한계점 및 향후 연구

7. **참고자료 및 코드**
   - 데이터 출처
   - GitHub 링크 (Public)

---

## 🔗 중요 링크

### 데이터 출처
- **KOBIS API**: https://www.kobis.or.kr/kobisopenapi/homepg/main/main.do
- **네이버 영화**: https://movie.naver.com/

### 기술 문서
- **Pandas**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/
- **KoNLPy**: https://konlpy.org/
- **Selenium**: https://selenium-python.readthedocs.io/

### 프로젝트 관리
- **GitHub**: (여기에 레포지토리 URL 추가 예정)
- **원격수업 사이트**: https://eclass.dongyang.ac.kr/

---

## 💡 핵심 메모

### 중간고사 피드백 반영사항
1. ✅ 데이터량 명확화 (300편 + 15,000개 리뷰)
2. ✅ 성공 기준 정의 (관객수 300만 이상)
3. ✅ 가설 설정 추가 (4개)
4. ✅ 분석 범위 조정 (Kaggle 제외)
5. ✅ 해석 가능한 모델 추가 (Logistic Regression)

### 가이드 요구사항 체크리스트
- [x] 2.1 표지 및 기본정보
- [x] 2.2 주제 선정 이유 및 배경
- [x] 2.3 데이터 수집 계획
- [x] 2.4 데이터 전처리 계획
- [x] 2.5 분석 도구 및 기술 스택
- [x] 2.6 기대 결과 및 활용 방안
- [x] 2.7 일정 계획
- [x] 2.8 참고문헌 및 출처

### 기말고사 필수 제출물
- [ ] 최종 보고서 PDF (20페이지 내외)
- [ ] 발표 PPT (15~20슬라이드)
- [ ] GitHub Public Repository (README 작성)
- [ ] 주요 코드 Jupyter Notebook (실행 가능)
- [ ] 시각화 파일 (PNG/JPG, 15개)
- [ ] 최종 데이터셋 CSV

---

## 🆘 트러블슈팅 빠른 참조

### KOBIS API 오류
**증상**: `ERROR - KOBIS_API_KEY가 설정되지 않았습니다.`
**해결**: `.env` 파일 확인, API 키 재입력

### ChromeDriver 오류
**증상**: `WebDriverException: 'chromedriver' executable...`
**해결**: `pip install --upgrade webdriver-manager`

### 메모리 부족
**증상**: `MemoryError: Unable to allocate array`
**해결**: 수집 대상 축소 (300편 → 100편)

### 네이버 크롤링 차단
**증상**: `WARNING - 영화 검색 결과 없음`
**해결**: delay 시간 증가 (2.0 → 3.0초), headless=False 설정

---

## 📞 연락처 및 문의

**학생 정보**
- 이름: 조은성
- 학번: 20232678
- 학과: 인공지능소프트웨어 [QB]

**과목 정보**
- 과목명: 빅데이터응용프로그래밍
- 학기: 2025년도 2학기
- 제출일: (원격수업 사이트 공지 참조)

---

## 🎯 다음 작업 시작하기

### 즉시 실행할 명령어

```bash
# 1. 프로젝트 폴더로 이동
cd "C:\Users\asus\DMU\2-sophomore\2st-semester\빅데이터\korean-movie-analysis"

# 2. 빠른 시작 가이드 확인
type QUICKSTART.md

# 3. 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 4. 패키지 설치
pip install -r requirements.txt

# 5. 환경변수 설정
copy .env.example .env
notepad .env

# 6. 테스트 실행
cd src
python test_collection.py
```

### 다음 대화 시작할 때

**상황 복원을 위한 메시지**:
```
"한국영화 성공 공식 분석 프로젝트를 진행 중입니다.
현재 데이터 수집 코드 작성이 완료되었고,
다음 단계로 [실제 데이터 수집 / 전처리 / 분석]을 진행하려고 합니다.
PROJECT_SUMMARY.md를 참고해서 이어서 진행해주세요."
```

---

**마지막 업데이트**: 2024-11-05
**진행률**: 20% (1주차 완료, 데이터 수집 준비 완료)
**다음 마일스톤**: 실제 데이터 수집 실행 (KOBIS + 네이버)
