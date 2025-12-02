# 한국영화 성공 공식 분석 프로젝트

## 프로젝트 개요
데이터 기반으로 한국영화의 흥행 성공 요인을 분석하는 빅데이터 응용 프로젝트

**분석 기간**: 2019-2024년
**목표 데이터**: 300편 영화 + 15,000개 리뷰

## 주요 연구 질문
1. 한국 영화의 흥행 성공을 결정짓는 주요 요인은?
2. 계절별/장르별 개봉 전략이 흥행에 미치는 영향은?
3. 관객 리뷰 감성과 실제 흥행 성과 간 상관관계는?

## 가설
- H1: 여름/겨울 성수기 개봉 영화가 봄/가을보다 평균 관객수 30% 이상 높다
- H2: 액션/SF 장르가 드라마/멜로보다 흥행 성공률 2배 높다
- H3: 네이버 평점 8.0 이상 영화는 7.0 이하 대비 흥행 성공률 5배 높다
- H4: 긍정 리뷰 비율 70% 이상 영화는 흥행 성공 확률 80% 이상이다

## 데이터 출처
- **KOBIS** (영화진흥위원회): 박스오피스 공식 통계
- **네이버 영화**: 평점 및 관객 리뷰

## 기술 스택
- Python 3.8+
- pandas, numpy
- requests, BeautifulSoup4, selenium
- scikit-learn
- matplotlib, seaborn
- KoNLPy

## 프로젝트 구조
```
korean-movie-analysis/
├── data/
│   ├── raw/              # 원본 데이터
│   ├── processed/        # 전처리 데이터
│   └── final/            # 최종 분석 데이터
├── notebooks/            # Jupyter Notebooks
├── src/                  # Python 소스 코드
├── visualizations/       # 시각화 결과
├── models/              # 학습된 모델
└── reports/             # 보고서
```

## 작성자
- 이름: 조은성
- 학번: 20232678
- 학과: 인공지능소프트웨어 [QB]

## License
Educational Project for DMU Big Data Programming Course
