"""
네이버 평점 및 성별 데이터 병합 및 분석
- 평점: 실관람객, 네티즌, 평론가
- 성별: 남녀 평점 차이, 성별 비율
- 시나리오 5 기준으로 성공/실패 분류
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def clean_rating_value(value):
    """평점 값 정리 (8.881 -> 8.88)"""
    if pd.isna(value):
        return np.nan

    if isinstance(value, str):
        # 마지막 '1' 제거
        value = value.rstrip('1')
        try:
            return float(value)
        except:
            return np.nan

    return float(value)


def merge_rating_data():
    """평점 및 성별 데이터 병합"""

    base_path = Path(__file__).parent.parent

    # 1. 데이터 로드
    logger.info("\n" + "=" * 80)
    logger.info("📂 데이터 로드 중...")
    logger.info("=" * 80)

    movies_file = base_path / 'data' / 'processed' / 'korean_movies_with_star_power.csv'
    ratings_file = base_path / 'data' / 'raw' / 'naver_ratings_220.csv'

    movies_df = pd.read_csv(movies_file, encoding='utf-8-sig')
    ratings_df = pd.read_csv(ratings_file, encoding='utf-8-sig')

    logger.info(f"  기존 영화 데이터: {len(movies_df)}편")
    logger.info(f"  평점 데이터: {len(ratings_df)}편")

    # 2. 평점 데이터 정리
    logger.info("\n" + "=" * 80)
    logger.info("🧹 평점 데이터 정리 중...")
    logger.info("=" * 80)

    # 빈 행 제거
    ratings_df = ratings_df.dropna(how='all')
    ratings_df = ratings_df[ratings_df['movie_name'].notna()]

    logger.info(f"  정리 후: {len(ratings_df)}편")

    # 평점 값 정리
    rating_columns = [
        'viewer_total', 'viewer_male', 'viewer_female',
        'netizen_total', 'netizen_male', 'netizen_female',
        'critic_rating_avg'
    ]

    for col in rating_columns:
        if col in ratings_df.columns:
            ratings_df[col] = ratings_df[col].apply(clean_rating_value)

    # 비율 숫자 변환
    ratio_columns = [
        'viewer_ratio_male', 'viewer_ratio_female',
        'netizen_ratio_male', 'netizen_ratio_female'
    ]

    for col in ratio_columns:
        if col in ratings_df.columns:
            ratings_df[col] = pd.to_numeric(ratings_df[col], errors='coerce')

    # 3. 병합
    logger.info("\n" + "=" * 80)
    logger.info("🔗 데이터 병합 중...")
    logger.info("=" * 80)

    rating_cols = [
        'movie_name', 'viewer_total', 'viewer_male', 'viewer_female',
        'netizen_total', 'netizen_male', 'netizen_female',
        'viewer_ratio_male', 'viewer_ratio_female',
        'netizen_ratio_male', 'netizen_ratio_female',
        'critic_rating_avg', 'critic_rating_count'
    ]

    ratings_subset = ratings_df[rating_cols].copy()

    merged_df = movies_df.merge(
        ratings_subset,
        left_on='movieNm',
        right_on='movie_name',
        how='left'
    )

    merged_df = merged_df.drop(columns=['movie_name'])

    logger.info(f"  병합 완료: {len(merged_df)}편")

    # 4. 성별 파생 변수 생성
    logger.info("\n" + "=" * 80)
    logger.info("🎭 성별 분석 변수 생성 중...")
    logger.info("=" * 80)

    # 실관람객 남녀 평점 차이
    merged_df['viewer_gender_gap'] = merged_df['viewer_male'] - merged_df['viewer_female']

    # 네티즌 남녀 평점 차이
    merged_df['netizen_gender_gap'] = merged_df['netizen_male'] - merged_df['netizen_female']

    # 성별 선호도 (절댓값이 클수록 성별 차이 큼)
    merged_df['viewer_gender_gap_abs'] = merged_df['viewer_gender_gap'].abs()
    merged_df['netizen_gender_gap_abs'] = merged_df['netizen_gender_gap'].abs()

    # 여성 선호 여부 (gap < 0이면 여성이 더 높은 평점)
    merged_df['female_preferred'] = (merged_df['viewer_gender_gap'] < -0.1).astype(int)

    logger.info("  생성된 성별 분석 변수:")
    logger.info("    - viewer_gender_gap: 실관람객 남녀 평점 차이")
    logger.info("    - netizen_gender_gap: 네티즌 남녀 평점 차이")
    logger.info("    - viewer_gender_gap_abs: 성별 평점 차이 절댓값")
    logger.info("    - female_preferred: 여성 선호 영화 여부")

    # 5. 시나리오 5 분류
    logger.info("\n" + "=" * 80)
    logger.info("🎯 시나리오 5 성공/실패 분류...")
    logger.info("=" * 80)

    COMMERCIAL_THRESHOLD = 4_000_000
    INDIE_THRESHOLD = 380_000

    def classify_movie_type(audience):
        return 'commercial' if audience >= COMMERCIAL_THRESHOLD else 'indie'

    def classify_success(row):
        audience = row['audiAcc']
        movie_type = row['movie_type']

        if movie_type == 'commercial':
            return 1 if audience >= COMMERCIAL_THRESHOLD else 0
        else:
            return 1 if audience >= INDIE_THRESHOLD else 0

    merged_df['movie_type'] = merged_df['audiAcc'].apply(classify_movie_type)
    merged_df['success'] = merged_df.apply(classify_success, axis=1)

    # 통계
    total = len(merged_df)
    commercial = (merged_df['movie_type'] == 'commercial').sum()
    indie = (merged_df['movie_type'] == 'indie').sum()
    success = merged_df['success'].sum()

    logger.info(f"  상업 영화: {commercial}편 (400만+)")
    logger.info(f"  독립 영화: {indie}편 (38만+)")
    logger.info(f"  전체 성공: {success}편 ({success/total*100:.1f}%)")

    # 6. 평점 및 성별 통계
    logger.info("\n" + "=" * 80)
    logger.info("📊 평점 및 성별 데이터 통계")
    logger.info("=" * 80)

    viewer_count = merged_df['viewer_total'].notna().sum()
    netizen_count = merged_df['netizen_total'].notna().sum()
    critic_count = merged_df['critic_rating_avg'].notna().sum()

    logger.info(f"\n  [평점 수집 현황]")
    logger.info(f"  실관람객: {viewer_count}편 ({viewer_count/total*100:.1f}%)")
    logger.info(f"  네티즌: {netizen_count}편 ({netizen_count/total*100:.1f}%)")
    logger.info(f"  평론가: {critic_count}편 ({critic_count/total*100:.1f}%)")

    logger.info(f"\n  [평점 평균]")
    logger.info(f"  실관람객: {merged_df['viewer_total'].mean():.2f}")
    logger.info(f"  네티즌: {merged_df['netizen_total'].mean():.2f}")
    logger.info(f"  평론가: {merged_df['critic_rating_avg'].mean():.2f}")

    # 성별 평점 차이 분석
    gap_data = merged_df[merged_df['viewer_gender_gap'].notna()]

    if len(gap_data) > 0:
        logger.info(f"\n  [성별 평점 차이 - 실관람객]")
        logger.info(f"  평균 차이: {gap_data['viewer_gender_gap'].mean():.2f}")
        logger.info(f"  남성 선호 (gap > 0.1): {(gap_data['viewer_gender_gap'] > 0.1).sum()}편")
        logger.info(f"  여성 선호 (gap < -0.1): {(gap_data['viewer_gender_gap'] < -0.1).sum()}편")
        logger.info(f"  중립 (|gap| <= 0.1): {(gap_data['viewer_gender_gap'].abs() <= 0.1).sum()}편")

        # 여성 관객 비율 평균
        female_ratio_mean = merged_df['viewer_ratio_female'].mean()
        logger.info(f"\n  [성별 비율]")
        logger.info(f"  평균 여성 관객 비율: {female_ratio_mean:.1f}%")
        logger.info(f"  평균 남성 관객 비율: {merged_df['viewer_ratio_male'].mean():.1f}%")

    # 7. 저장
    logger.info("\n" + "=" * 80)
    logger.info("💾 최종 데이터 저장 중...")
    logger.info("=" * 80)

    output_file = base_path / 'data' / 'processed' / 'korean_movies_final.csv'
    merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    logger.info(f"  저장 완료: {output_file}")
    logger.info(f"  총 컬럼: {len(merged_df.columns)}개")
    logger.info(f"  총 영화: {len(merged_df)}편")

    # 8. 주요 컬럼 목록
    logger.info("\n" + "=" * 80)
    logger.info("📋 분석 가능한 주요 변수")
    logger.info("=" * 80)

    logger.info("\n  [평점 변수]")
    logger.info("    - viewer_total, viewer_male, viewer_female")
    logger.info("    - netizen_total, netizen_male, netizen_female")
    logger.info("    - critic_rating_avg")

    logger.info("\n  [성별 변수]")
    logger.info("    - viewer_ratio_male, viewer_ratio_female")
    logger.info("    - netizen_ratio_male, netizen_ratio_female")
    logger.info("    - viewer_gender_gap (남녀 평점 차이)")
    logger.info("    - female_preferred (여성 선호 영화)")

    logger.info("\n  [스타 파워]")
    logger.info("    - director_star_power, actor_star_power, total_star_power")

    logger.info("\n  [흥행 실적]")
    logger.info("    - audiAcc (누적 관객 수)")
    logger.info("    - movie_type (commercial/indie)")
    logger.info("    - success (성공 여부)")

    logger.info("\n" + "=" * 80)
    logger.info("✅ 모든 작업 완료!")
    logger.info("=" * 80)

    return merged_df


if __name__ == '__main__':
    df = merge_rating_data()
