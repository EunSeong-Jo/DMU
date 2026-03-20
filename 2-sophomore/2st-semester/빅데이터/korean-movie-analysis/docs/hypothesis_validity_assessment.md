# 현재 6가지 가설의 유의미성 평가 및 개선 방안

## 📊 현재 6가지 가설 평가

### ✅ **유의미한 가설 (실무 활용 가능)**

#### **H1: 계절별 개봉 효과**
- **평가**: ⭐⭐⭐⭐⭐ (매우 유의미)
- **이유**:
  - 배급사가 **직접 통제 가능한 변수** (개봉 시기 선택 가능)
  - 실무에서 가장 중요한 전략적 의사결정 요소
  - 경쟁작 회피, 성수기 공략 등 실제 비즈니스 영향 큼
- **한계**:
  - 역인과 관계 가능성 (좋은 영화를 성수기에 개봉)
  - 계절 효과 vs 경쟁 효과 분리 어려움

#### **H2: 장르별 성공률**
- **평가**: ⭐⭐⭐⭐ (유의미)
- **이유**:
  - 기획 단계에서 활용 가능 (장르 선택)
  - 시장 트렌드 파악 가능
  - 투자 결정에 중요한 지표
- **한계**:
  - 장르 분류 모호함 (복합 장르 처리)
  - 장르 내 품질 편차 큼 (액션도 천차만별)
  - **장르는 결과가 아닌 선택의 문제**

#### **H3: 평점과 성공률**
- **평가**: ⭐⭐ (제한적 유의미)
- **이유**:
  - 영화 품질의 지표로 활용 가능
  - 입소문 효과 검증 가능
- **치명적 한계**:
  - **역인과 관계**: 흥행 → 평점 (성공한 영화에 사람들이 몰려 평점 많이 남김)
  - **사후 지표**: 평점은 개봉 후 생성되므로 사전 예측 불가
  - **순환 논리**: "성공하면 평점 높다" vs "평점 높으면 성공한다" 구분 안 됨
- **개선 방안**:
  - 시계열 분석 필요 (개봉 1주차 평점 vs 최종 관객수)
  - 평점 증가 속도, 평점 분산 등 메타 지표 활용

### ⚠️ **유의미하지만 개선 필요한 가설**

#### **H4: 관람등급과 관객수**
- **평가**: ⭐⭐⭐ (보통)
- **이유**:
  - 타겟 관객층 크기 영향 분석 가능
  - 기획 단계 의사결정 지표
- **한계**:
  - **관람등급은 내용의 결과물** (선택 불가)
  - 전체관람가 vs 청불은 영화 내용 자체가 다름
  - 단순 비교는 의미 제한적
- **개선 방안**:
  - 장르별 관람등급 효과 분석 (액션은 15세, 드라마는 전체관람가 등)

#### **H5: 상영시간과 흥행**
- **평가**: ⭐⭐⭐ (보통)
- **이유**:
  - 상영 회차, 관람 피로도 영향 파악 가능
  - 일부 조절 가능 (편집)
- **한계**:
  - **상영시간은 내용의 결과** (150분짜리 서사를 90분으로 못 줄임)
  - 장르별 최적 상영시간 상이 (애니메이션 90분 vs 서사극 150분)
- **개선 방안**:
  - 장르별 최적 상영시간 도출

#### **H6: 장르별 성별 선호도**
- **평가**: ⭐⭐⭐ (보통)
- **이유**:
  - 마케팅 타겟팅에 활용 가능
  - 시장 세분화 전략 수립 가능
- **한계**:
  - **성별 선호는 장르의 결과** (로맨스를 만들면 여성 선호가 자연스러움)
  - 인과관계 불명확
  - 성별 이분법 한계 (실제 관객은 다양)
- **개선 방안**:
  - 성별 타겟팅 마케팅 효과 분석 (광고비 배분)

---

## 🚨 현재 가설의 근본적 문제점

### **1. 역인과 관계 (Reverse Causality)**
```
실제: 영화 품질 좋음 → 흥행 성공 → 평점 높음
오해: 평점 높음 → 흥행 성공
```

### **2. 내생성 문제 (Endogeneity)**
- 장르, 관람등급, 상영시간은 **영화 내용의 결과물**
- 이들을 조작해서 흥행을 높일 수 없음
- 예: "청불을 전체관람가로 바꾸면 관객수 2배" → 불가능

### **3. 누락 변수 편의 (Omitted Variable Bias)**
**진짜 중요한 변수들이 빠져 있음:**
- 마케팅 비용 💰
- 배우/감독 스타파워 ⭐
- 제작비 규모 💵
- 스크린 수 (배급력) 🎬
- 경쟁작 현황 🎯
- SNS 버즈량 📱
- 예고편 조회수 👀

### **4. 예측력 vs 설명력 혼동**
- 현재 가설: **사후 설명** (왜 성공했나?)
- 실무 필요: **사전 예측** (성공할까?)

---

## 💡 한국 영화 성공 공식을 위한 개선된 분석 프레임워크

### **📍 Phase 1: 통제 가능 변수 (전략적 의사결정)**

#### **1. 개봉 전략 분석** ⭐⭐⭐⭐⭐
**가설**:
- 경쟁작 회피 효과
- 연휴/방학 효과
- 개봉 스크린 수 전략

**분석 방법**:
```python
# 개봉 주 경쟁 강도 계산
competition_score = sum(other_movies_audience) / total_screens
success_rate_by_competition = analyze(competition_score, audience)

# 연휴 효과
holiday_effect = audience_with_holiday / audience_without_holiday
```

**실무 활용**:
- 배급사가 개봉일 선택 시 활용
- 경쟁 회피 vs 성수기 공략 trade-off 분석

---

#### **2. 마케팅 효율성 분석** ⭐⭐⭐⭐⭐
**가설**:
- 예고편 조회수 vs 흥행
- SNS 언급량 vs 흥행
- 배우 인지도 vs 흥행

**현재 수집 가능 데이터**:
- Naver 영화 페이지 조회수 (간접 지표)
- 포털 검색량 (Naver 트렌드)
- 배우/감독 필모그래피 (KOBIS)

**분석 방법**:
```python
# 개봉 전 버즈 vs 1주차 관객
pre_release_buzz = naver_page_views + search_volume
week1_audience = first_week_audience
effectiveness = week1_audience / pre_release_buzz

# 입소문 효과 (1주차 → 최종)
word_of_mouth = final_audience / week1_audience
```

**실무 활용**:
- 마케팅 예산 배분
- 효과적인 홍보 채널 선택

---

#### **3. 스타파워 효과 분석** ⭐⭐⭐⭐
**가설**:
- 주연 배우 과거 흥행력 vs 현재 흥행
- 감독 과거 평점 vs 현재 흥행

**현재 보유 데이터**:
- KOBIS에서 수집한 directors, actors

**분석 방법**:
```python
# 배우/감독의 과거 평균 관객수 계산
actor_past_avg = mean(actor_previous_movies_audience)
director_past_avg = mean(director_previous_movies_audience)

# 스타파워 점수
star_power_score = 0.6 * actor_past_avg + 0.4 * director_past_avg

# 현재 흥행과 상관관계
correlation(star_power_score, current_audience)
```

**실무 활용**:
- 캐스팅 의사결정
- 제작비 배분 (스타 개런티 vs 제작비)

---

### **📍 Phase 2: 시장 트렌드 분석 (전략적 인사이트)**

#### **4. 장르별 시장 포화도 분석** ⭐⭐⭐⭐
**기존 H2 개선**:
```python
# 연도별 장르 공급량 vs 수요
genre_supply_by_year = count(genre, year)
genre_demand_by_year = mean(audience, genre, year)

# 포화도 = 공급 / 수요
saturation = genre_supply_by_year / genre_demand_by_year

# 블루오션 장르 도출
blue_ocean_genres = genres[saturation < 0.5]
```

**실무 활용**:
- 기획 단계 장르 선택
- 차별화 전략 수립

---

#### **5. 시계열 트렌드 분석** ⭐⭐⭐⭐
**가설**:
- OTT 확산 후 극장 관객 변화
- 코로나 전후 관객 패턴 변화
- 장르 선호도 변화 추세

**분석 방법**:
```python
# 연도별 트렌드
yearly_trend = audience_by_year
pre_covid = mean(audience[2019])
post_covid = mean(audience[2022:2024])
covid_impact = (post_covid - pre_covid) / pre_covid

# 회복 추세
recovery_rate = (audience_2024 - audience_2020) / (audience_2019 - audience_2020)
```

---

### **📍 Phase 3: 예측 모델 구축 (실전 활용)**

#### **6. 통합 예측 모델** ⭐⭐⭐⭐⭐

**독립 변수 (예측 가능한 것만)**:
```python
features = {
    # 통제 가능
    'release_month': 개봉월,
    'release_screens': 개봉 스크린 수,
    'genre': 장르,

    # 측정 가능
    'director_past_avg': 감독 과거 평균 관객수,
    'actor_star_power': 주연 배우 스타파워 점수,
    'competition_score': 개봉 주 경쟁 강도,
    'pre_release_buzz': 개봉 전 버즈량,

    # 영화 속성
    'watch_grade': 관람등급,
    'runtime': 상영시간,
    'production_year': 제작 연도 (트렌드)
}

target = '관객수' or '성공 여부(300만 이상)'
```

**모델링**:
```python
# Random Forest (변수 중요도 분석)
rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)
feature_importance = rf_model.feature_importances_

# 결과: 어떤 변수가 가장 중요한가?
# 예상: 스타파워(30%), 개봉시기(20%), 스크린수(15%), ...
```

---

## 🎯 최종 권장 분석 로드맵

### **현실적 접근 (현재 데이터로 가능)**

#### **Step 1: 기본 분석 (Week 2-3)**
✅ H1: 개봉 시기 효과 (유지)
✅ H2: 장르별 성공률 + 포화도 분석 (개선)
✅ 스타파워 분석 (추가) - directors, actors 활용
✅ 경쟁 강도 분석 (추가) - 개봉일 기준 계산

#### **Step 2: 심화 분석 (Week 3-4)**
⭐ 시계열 트렌드 (코로나 전후)
⭐ 통합 예측 모델 (Random Forest)
⭐ 변수 중요도 랭킹

#### **Step 3: 성공 공식 도출 (Week 4-5)**
```
한국 영화 성공 확률 =
  0.3 * 스타파워 점수
+ 0.2 * 개봉 시기 점수 (성수기 + 경쟁 회피)
+ 0.15 * 장르 트렌드 점수
+ 0.15 * 개봉 스크린 수
+ 0.1 * 사전 버즈량
+ 0.1 * 기타 (관람등급, 상영시간)
```

---

### **이상적 접근 (추가 데이터 필요)**

만약 추가 데이터를 수집할 수 있다면:

1. **마케팅 비용** (영화진흥위원회 공개 데이터)
2. **제작비** (일부 영화 공개)
3. **개봉 스크린 수** (KOBIS API에 일부 포함)
4. **SNS 버즈량** (Twitter/Instagram API)
5. **예고편 조회수** (YouTube API)
6. **포털 검색량** (Naver DataLab API)

이 데이터들이 있으면 **진짜 예측력 있는 모델** 구축 가능

---

## 📝 결론 및 제안

### **현재 6가지 가설 평가**

| 가설 | 유의미성 | 실무 활용 | 문제점 |
|-----|---------|---------|--------|
| H1 (개봉시기) | ⭐⭐⭐⭐⭐ | 높음 | 경쟁 효과 분리 필요 |
| H2 (장르) | ⭐⭐⭐⭐ | 보통 | 포화도 분석 추가 필요 |
| H3 (평점) | ⭐⭐ | 낮음 | 역인과 문제 심각 |
| H4 (관람등급) | ⭐⭐⭐ | 낮음 | 통제 불가능 |
| H5 (상영시간) | ⭐⭐⭐ | 낮음 | 통제 불가능 |
| H6 (성별선호) | ⭐⭐⭐ | 보통 | 자명한 결과 |

### **권장 사항**

#### **Option 1: 현재 가설 유지 + 보완** (안전)
- H1, H2는 그대로 진행
- H3는 "시계열 분석"으로 개선 (개봉 초기 평점 vs 최종 관객)
- H4, H5, H6는 "보조 분석"으로 격하
- **추가**: 스타파워 분석, 경쟁 강도 분석

#### **Option 2: 프레임워크 재설계** (야심적)
기존 6가지 폐기하고:
1. 개봉 전략 효과 (시기 + 경쟁 회피)
2. 스타파워 효과 (배우 + 감독)
3. 장르 트렌드 및 포화도
4. 시계열 변화 (코로나, OTT 영향)
5. 통합 예측 모델
6. 성공 공식 도출

**추천: Option 1** (학부 프로젝트로는 충분, 시간 대비 효과 좋음)

---

## 💪 실행 가능한 Next Step

**현재 데이터로 즉시 추가 분석 가능:**

```python
# 1. 스타파워 분석
directors_performance = analyze_director_filmography()
actors_performance = analyze_actor_filmography()

# 2. 경쟁 강도 분석
competition_by_date = calculate_competition_intensity()

# 3. 시계열 트렌드
yearly_trend = analyze_yearly_patterns()
covid_impact = compare_pre_post_covid()

# 4. 통합 예측 모델
success_prediction_model = build_random_forest_model()
feature_importance_ranking = get_feature_importance()
```

**이것만 추가해도 프로젝트 수준이 논문급으로 상승합니다!**
