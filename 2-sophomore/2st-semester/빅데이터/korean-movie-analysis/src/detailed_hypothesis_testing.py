"""
가설 검증 상세 분석
H1: 계절별 흥행 차이
H2: 장르별 성공률 비교
H3: 평점-흥행 관계 분석
H4: 긍정 리뷰 비율과 성공률
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 경로 설정
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'processed'
VIZ_DIR = BASE_DIR / 'visualizations'
REPORT_DIR = BASE_DIR / 'reports'

VIZ_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("="*60)
print("가설 검증 상세 분석")
print("="*60)

# 데이터 로드
top10_df = pd.read_csv(DATA_DIR / 'korean_movies_final.csv')
all_2022 = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'korean_movies_2022.csv')
all_2023 = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'korean_movies_2023.csv')
all_2024 = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'korean_movies_2024.csv')

# 전체 영화 병합
all_movies = pd.concat([all_2022, all_2023, all_2024], ignore_index=True)

# 성인물 제외
all_movies = all_movies[~all_movies['genres'].str.contains('성인물\\(에로\\)', na=False)].copy()

print(f"\n[데이터 로드]")
print(f"TOP 10 영화: {len(top10_df)}편")
print(f"전체 영화 (2022-2024, 성인물 제외): {len(all_movies)}편")

# TOP 10 여부 표시
all_movies['is_top10'] = all_movies['movieCd'].isin(top10_df['movieCd']).astype(int)

print(f"전체 영화 중 TOP 10: {all_movies['is_top10'].sum()}편")
print(f"성공률: {all_movies['is_top10'].mean()*100:.2f}%")

print("\n" + "="*60)
print("H1: 계절별 흥행 차이 검증")
print("="*60)

# 개봉일 파싱
top10_df['openDt'] = pd.to_datetime(top10_df['openDt'], format='%Y%m%d', errors='coerce')
all_movies['openDt'] = pd.to_datetime(all_movies['openDt'], format='%Y%m%d', errors='coerce')

# 계절 분류 함수
def get_season(month):
    if month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    elif month in [9, 10, 11]:
        return '가을'
    else:  # 12, 1, 2
        return '겨울'

# TOP 10 영화 계절 분석
top10_df['month'] = top10_df['openDt'].dt.month
top10_df['season'] = top10_df['month'].apply(get_season)

season_counts_top10 = top10_df['season'].value_counts()
season_pct_top10 = (season_counts_top10 / len(top10_df) * 100).round(1)

print(f"\n[TOP 10 영화의 계절별 분포]")
for season in ['봄', '여름', '가을', '겨울']:
    count = season_counts_top10.get(season, 0)
    pct = season_pct_top10.get(season, 0)
    print(f"  {season}: {count}편 ({pct}%)")

# 전체 영화 계절 분석
all_movies['month'] = all_movies['openDt'].dt.month
all_movies['season'] = all_movies['month'].apply(get_season)

season_success = all_movies.groupby('season').agg({
    'is_top10': ['sum', 'count', 'mean']
}).round(4)

season_success.columns = ['TOP10_count', 'total_count', 'success_rate']
season_success['success_rate_pct'] = (season_success['success_rate'] * 100).round(2)
season_success = season_success.sort_values('success_rate', ascending=False)

print(f"\n[계절별 성공률 (2022-2024)]")
print(season_success)

# 여름+겨울 vs 봄+가을 비교
summer_winter = all_movies[all_movies['season'].isin(['여름', '겨울'])]
spring_fall = all_movies[all_movies['season'].isin(['봄', '가을'])]

sw_success_rate = summer_winter['is_top10'].mean()
sf_success_rate = spring_fall['is_top10'].mean()

print(f"\n[여름+겨울 vs 봄+가을 비교]")
print(f"  여름+겨울 성공률: {sw_success_rate*100:.2f}% ({summer_winter['is_top10'].sum()}편/{len(summer_winter)}편)")
print(f"  봄+가을 성공률: {sf_success_rate*100:.2f}% ({spring_fall['is_top10'].sum()}편/{len(spring_fall)}편)")
print(f"  차이: {(sw_success_rate - sf_success_rate)*100:.2f}%p")

# 카이제곱 검정
from scipy.stats import chi2_contingency

contingency = pd.crosstab(
    all_movies['season'].isin(['여름', '겨울']),
    all_movies['is_top10']
)

chi2, p_value_season, dof, expected = chi2_contingency(contingency)

print(f"\n[통계적 유의성 검정 (카이제곱)]")
print(f"  카이제곱 통계량: {chi2:.4f}")
print(f"  p-value: {p_value_season:.4f}")
if p_value_season < 0.05:
    print(f"  → 유의미한 차이 있음 (p<0.05)")
else:
    print(f"  → 유의미한 차이 없음 (p>=0.05)")

print(f"\n[H1 검증 결과]")
if abs((sw_success_rate - sf_success_rate)) >= 0.30:
    print(f"  [O] 채택: 여름+겨울이 봄+가을보다 30%p 이상 높음")
else:
    print(f"  [X] 기각: 차이가 30%p 미만 ({abs((sw_success_rate - sf_success_rate)*100):.2f}%p)")

# 시각화
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 계절별 TOP 10 분포
axes[0].bar(season_counts_top10.index, season_counts_top10.values,
            color=['lightcoral', 'gold', 'orange', 'skyblue'])
axes[0].set_title('계절별 TOP 10 영화 분포 (2014-2024)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('영화 수 (편)')
for i, (season, count) in enumerate(season_counts_top10.items()):
    axes[0].text(i, count + 2, f'{count}편\n({season_pct_top10[season]}%)',
                ha='center', fontsize=10)

# 계절별 성공률
axes[1].bar(season_success.index, season_success['success_rate_pct'],
            color=['lightcoral', 'gold', 'orange', 'skyblue'])
axes[1].set_title('계절별 흥행 성공률 (2022-2024)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('성공률 (%)')
axes[1].axhline(y=all_movies['is_top10'].mean()*100, color='red',
                linestyle='--', label=f'전체 평균: {all_movies["is_top10"].mean()*100:.2f}%')
axes[1].legend()

for i, (season, row) in enumerate(season_success.iterrows()):
    axes[1].text(i, row['success_rate_pct'] + 0.3,
                f'{row["success_rate_pct"]}%\n({int(row["TOP10_count"])}/{int(row["total_count"])})',
                ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(VIZ_DIR / 'h1_seasonal_analysis.png', dpi=300, bbox_inches='tight')
print(f"\n[저장] {VIZ_DIR / 'h1_seasonal_analysis.png'}")

print("\n" + "="*60)
print("H2: 장르별 성공률 비교")
print("="*60)

# 장르 분리 및 성공률 계산
all_genres = []

for idx, row in all_movies.iterrows():
    genres = str(row['genres']).split(',') if pd.notna(row['genres']) else []
    is_top10 = row['is_top10']

    for genre in genres:
        genre = genre.strip()
        if genre:
            all_genres.append({
                'genre': genre,
                'is_top10': is_top10
            })

genre_df = pd.DataFrame(all_genres)

# 장르별 성공률
genre_stats = genre_df.groupby('genre').agg({
    'is_top10': ['sum', 'count', 'mean']
}).round(4)

genre_stats.columns = ['success_count', 'total_count', 'success_rate']
genre_stats['success_rate_pct'] = (genre_stats['success_rate'] * 100).round(2)

# 최소 10편 이상 개봉한 장르만
genre_stats = genre_stats[genre_stats['total_count'] >= 10].copy()
genre_stats = genre_stats.sort_values('success_rate', ascending=False)

print(f"\n[장르별 성공률 (10편 이상)]")
print(genre_stats.head(15))

# 액션/SF vs 드라마/멜로 비교
action_sf = genre_df[genre_df['genre'].isin(['액션', 'SF'])]
drama_melo = genre_df[genre_df['genre'].isin(['드라마', '멜로/로맨스'])]

action_sf_rate = action_sf['is_top10'].mean()
drama_melo_rate = drama_melo['is_top10'].mean()

print(f"\n[액션/SF vs 드라마/멜로 비교]")
print(f"  액션/SF 성공률: {action_sf_rate*100:.2f}% ({action_sf['is_top10'].sum()}편/{len(action_sf)}편)")
print(f"  드라마/멜로 성공률: {drama_melo_rate*100:.2f}% ({drama_melo['is_top10'].sum()}편/{len(drama_melo)}편)")
print(f"  비율: {action_sf_rate / drama_melo_rate if drama_melo_rate > 0 else 0:.2f}배")

print(f"\n[H2 검증 결과]")
if action_sf_rate >= 2 * drama_melo_rate:
    print(f"  [O] 채택: 액션/SF가 드라마/멜로보다 2배 이상 성공률 높음")
else:
    print(f"  [X] 기각: 액션/SF가 드라마/멜로보다 2배 미만 ({action_sf_rate / drama_melo_rate if drama_melo_rate > 0 else 0:.2f}배)")

# 시각화
plt.figure(figsize=(12, 6))

top_genres = genre_stats.head(15).sort_values('success_rate_pct')
colors = ['coral' if genre in ['액션', 'SF'] else 'skyblue' if genre in ['드라마', '멜로/로맨스'] else 'lightgray'
          for genre in top_genres.index]

plt.barh(range(len(top_genres)), top_genres['success_rate_pct'], color=colors)
plt.yticks(range(len(top_genres)), top_genres.index)
plt.xlabel('성공률 (%)')
plt.title('장르별 흥행 성공률 Top 15 (2022-2024, 10편 이상)', fontsize=12, fontweight='bold')
plt.axvline(x=all_movies['is_top10'].mean()*100, color='red',
            linestyle='--', label=f'전체 평균: {all_movies["is_top10"].mean()*100:.2f}%')
plt.legend()

for i, (genre, row) in enumerate(top_genres.iterrows()):
    plt.text(row['success_rate_pct'] + 0.3, i,
            f'{row["success_rate_pct"]}% ({int(row["success_count"])}/{int(row["total_count"])})',
            va='center', fontsize=9)

plt.tight_layout()
plt.savefig(VIZ_DIR / 'h2_genre_success_rate.png', dpi=300, bbox_inches='tight')
print(f"\n[저장] {VIZ_DIR / 'h2_genre_success_rate.png'}")

print("\n" + "="*60)
print("H3: 평점-흥행 관계 상세 분석")
print("="*60)

# 평점 데이터가 있는 TOP 10 영화만
rating_df = top10_df[
    top10_df['viewer_total'].notna() &
    top10_df['audiAcc'].notna()
].copy()

print(f"\n[평점 데이터 보유 영화: {len(rating_df)}편]")

# 평점 구간 분류
rating_df['rating_level'] = pd.cut(
    rating_df['viewer_total'],
    bins=[0, 7.0, 8.0, 9.0, 10.0],
    labels=['7.0 미만', '7.0-8.0', '8.0-9.0', '9.0+']
)

# 구간별 평균 관객 수
rating_audience = rating_df.groupby('rating_level', observed=True).agg({
    'audiAcc': ['mean', 'count']
}).round(0)

rating_audience.columns = ['avg_audience', 'count']
rating_audience['avg_audience_million'] = (rating_audience['avg_audience'] / 10000).round(1)

print(f"\n[평점 구간별 평균 관객 수]")
print(rating_audience)

# 8.0 이상 vs 7.0 미만 비교
high_rating = rating_df[rating_df['viewer_total'] >= 8.0]
low_rating = rating_df[rating_df['viewer_total'] < 7.0]

if len(high_rating) > 0 and len(low_rating) > 0:
    high_avg = high_rating['audiAcc'].mean()
    low_avg = low_rating['audiAcc'].mean()

    print(f"\n[평점 8.0+ vs 7.0- 비교]")
    print(f"  평점 8.0+ 평균 관객: {high_avg/10000:.1f}만명 ({len(high_rating)}편)")
    print(f"  평점 7.0- 평균 관객: {low_avg/10000:.1f}만명 ({len(low_rating)}편)")
    print(f"  비율: {high_avg / low_avg if low_avg > 0 else 0:.2f}배")

    # t-test
    t_stat, p_value_rating = stats.ttest_ind(high_rating['audiAcc'], low_rating['audiAcc'])

    print(f"\n[통계적 유의성 검정 (t-test)]")
    print(f"  t-통계량: {t_stat:.4f}")
    print(f"  p-value: {p_value_rating:.4f}")
    if p_value_rating < 0.05:
        print(f"  → 유의미한 차이 있음 (p<0.05)")
    else:
        print(f"  → 유의미한 차이 없음 (p>=0.05)")

    print(f"\n[H3 검증 결과]")
    if high_avg >= 5 * low_avg:
        print(f"  [O] 채택: 평점 8.0+가 7.0-보다 5배 이상 관객 많음")
    else:
        print(f"  [X] 기각: 평점 8.0+가 7.0-보다 5배 미만 ({high_avg / low_avg if low_avg > 0 else 0:.2f}배)")
else:
    print(f"\n[경고] 비교 데이터 부족")
    print(f"  평점 8.0+ 영화: {len(high_rating)}편")
    print(f"  평점 7.0- 영화: {len(low_rating)}편")

# 시각화
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 평점-관객 수 산점도
axes[0].scatter(rating_df['viewer_total'], rating_df['audiAcc']/10000, alpha=0.6, s=100)
axes[0].set_xlabel('실관람객 평점')
axes[0].set_ylabel('누적 관객 수 (만명)')
axes[0].set_title(f'평점 vs 관객 수 (상관계수: {rating_df["viewer_total"].corr(rating_df["audiAcc"]):.3f})',
                  fontsize=12, fontweight='bold')

# 회귀선
z = np.polyfit(rating_df['viewer_total'], rating_df['audiAcc']/10000, 1)
p = np.poly1d(z)
axes[0].plot(rating_df['viewer_total'], p(rating_df['viewer_total']),
            "r--", alpha=0.8, linewidth=2)

# 평점 구간별 평균 관객
axes[1].bar(range(len(rating_audience)), rating_audience['avg_audience_million'],
            color='coral', alpha=0.7)
axes[1].set_xticks(range(len(rating_audience)))
axes[1].set_xticklabels(rating_audience.index)
axes[1].set_ylabel('평균 관객 수 (만명)')
axes[1].set_title('평점 구간별 평균 관객 수', fontsize=12, fontweight='bold')

for i, (level, row) in enumerate(rating_audience.iterrows()):
    axes[1].text(i, row['avg_audience_million'] + 10,
                f'{row["avg_audience_million"]}만\n({int(row["count"])}편)',
                ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(VIZ_DIR / 'h3_rating_audience_analysis.png', dpi=300, bbox_inches='tight')
print(f"\n[저장] {VIZ_DIR / 'h3_rating_audience_analysis.png'}")

print("\n" + "="*60)
print("H4: 긍정 리뷰 비율과 성공률")
print("="*60)

# 평점 8.0을 긍정으로 간주
rating_df['is_positive'] = (rating_df['viewer_total'] >= 8.0).astype(int)

positive_ratio = rating_df['is_positive'].mean()
print(f"\n[긍정 평가 비율 (8.0+)]")
print(f"  비율: {positive_ratio*100:.1f}% ({rating_df['is_positive'].sum()}편/{len(rating_df)}편)")

# 실관람객 평점 vs 네티즌 평점
if 'netizen_total' in rating_df.columns:
    rating_df['netizen_positive'] = (rating_df['netizen_total'] >= 8.0).astype(int)
    netizen_positive_ratio = rating_df['netizen_positive'].mean()

    print(f"\n[네티즌 긍정 평가 비율 (8.0+)]")
    print(f"  비율: {netizen_positive_ratio*100:.1f}% ({rating_df['netizen_positive'].sum()}편/{len(rating_df)}편)")

# 평점 기준별 성공률 (300만 이상을 성공으로 간주)
rating_df['box_office_success'] = (rating_df['audiAcc'] >= 3000000).astype(int)

positive_movies = rating_df[rating_df['is_positive'] == 1]
negative_movies = rating_df[rating_df['is_positive'] == 0]

if len(positive_movies) > 0 and len(negative_movies) > 0:
    positive_success_rate = positive_movies['box_office_success'].mean()
    negative_success_rate = negative_movies['box_office_success'].mean()

    print(f"\n[평점별 흥행 성공률 (300만+ 기준)]")
    print(f"  긍정(8.0+): {positive_success_rate*100:.1f}% ({positive_movies['box_office_success'].sum()}편/{len(positive_movies)}편)")
    print(f"  부정(8.0-): {negative_success_rate*100:.1f}% ({negative_movies['box_office_success'].sum()}편/{len(negative_movies)}편)")

    print(f"\n[H4 검증 결과]")
    if positive_ratio >= 0.70 and positive_success_rate >= 0.80:
        print(f"  [O] 채택: 긍정 비율 70%+이고 성공률 80%+")
    else:
        print(f"  [~] 부분 채택: 긍정 비율 {positive_ratio*100:.1f}%, 성공률 {positive_success_rate*100:.1f}%")
else:
    print(f"\n[경고] 비교 데이터 부족")

# 종합 결과 저장
print("\n" + "="*60)
print("가설 검증 종합 결과")
print("="*60)

results = {
    'H1': {
        '가설': '여름+겨울 > 봄+가을 (30%p 이상)',
        '실제_차이': f'{abs((sw_success_rate - sf_success_rate)*100):.2f}%p',
        'p_value': f'{p_value_season:.4f}',
        '결론': '채택' if abs((sw_success_rate - sf_success_rate)) >= 0.30 else '기각'
    },
    'H2': {
        '가설': '액션/SF > 드라마/멜로 (2배 이상)',
        '실제_비율': f'{action_sf_rate / drama_melo_rate if drama_melo_rate > 0 else 0:.2f}배',
        '결론': '채택' if action_sf_rate >= 2 * drama_melo_rate else '기각'
    },
    'H3': {
        '가설': '평점 8.0+ > 7.0- (5배 이상)',
        '실제_비율': f'{high_avg / low_avg if len(high_rating) > 0 and len(low_rating) > 0 and low_avg > 0 else 0:.2f}배',
        'p_value': f'{p_value_rating:.4f}' if len(high_rating) > 0 and len(low_rating) > 0 else 'N/A',
        '결론': '채택' if len(high_rating) > 0 and len(low_rating) > 0 and high_avg >= 5 * low_avg else '기각'
    },
    'H4': {
        '가설': '긍정 리뷰 70%+ = 성공 80%+',
        '긍정_비율': f'{positive_ratio*100:.1f}%',
        '성공률': f'{positive_success_rate*100:.1f}%' if len(positive_movies) > 0 else 'N/A',
        '결론': '채택' if positive_ratio >= 0.70 and positive_success_rate >= 0.80 else '부분 채택'
    }
}

print("\n[최종 검증 결과]")
for h, data in results.items():
    print(f"\n{h}: {data['가설']}")
    for key, value in data.items():
        if key != '가설':
            print(f"  {key}: {value}")

# 결과를 텍스트로 저장
with open(REPORT_DIR / 'hypothesis_testing_results.txt', 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("가설 검증 상세 결과\n")
    f.write("="*60 + "\n\n")

    for h, data in results.items():
        f.write(f"\n{h}: {data['가설']}\n")
        for key, value in data.items():
            if key != '가설':
                f.write(f"  {key}: {value}\n")

print(f"\n[저장] {REPORT_DIR / 'hypothesis_testing_results.txt'}")
print("\n" + "="*60)
print("분석 완료!")
print("="*60)
