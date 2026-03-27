"""
2019-2024년 신작만 필터링
- 재개봉/특별상영 제외
- 분석 대상 데이터셋 정제
"""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def filter_new_releases(input_path: str, output_path: str):
    """2019-2024년 신작만 필터링"""

    logger.info("="*60)
    logger.info("🎬 2019-2024년 신작 필터링 시작")
    logger.info("="*60)

    # 데이터 로드
    df = pd.read_csv(input_path)
    logger.info(f"원본 데이터: {len(df)}편")

    # 개봉일 파싱
    df['openDt'] = pd.to_datetime(df['openDt'], errors='coerce')
    df['year'] = df['openDt'].dt.year

    # 연도별 분포
    logger.info("\n연도별 영화 수 (필터링 전):")
    yearly = df['year'].value_counts().sort_index()
    for year, count in yearly.items():
        if pd.notna(year):
            logger.info(f"  {int(year)}년: {count}편")

    # 2019-2024년만 필터링
    filtered_df = df[(df['year'] >= 2019) & (df['year'] <= 2024)].copy()

    logger.info(f"\n필터링 결과: {len(filtered_df)}편 (2019-2024년)")

    # 필터링 후 연도별 분포
    logger.info("\n연도별 영화 수 (필터링 후):")
    yearly_filtered = filtered_df['year'].value_counts().sort_index()
    for year, count in yearly_filtered.items():
        logger.info(f"  {int(year)}년: {count}편")

    # 성공률 분석
    success_count = (filtered_df['success'] == 1).sum()
    success_rate = success_count / len(filtered_df) * 100
    logger.info(f"\n성공률 (300만+): {success_count}편 / {len(filtered_df)}편 = {success_rate:.1f}%")

    # 데이터 완성도
    logger.info("\n데이터 완성도:")
    logger.info(f"  스타파워: {filtered_df['total_star_power'].notna().sum()}편 ({filtered_df['total_star_power'].notna().sum()/len(filtered_df)*100:.1f}%)")
    logger.info(f"  평점: {filtered_df['rating'].notna().sum()}편 ({filtered_df['rating'].notna().sum()/len(filtered_df)*100:.1f}%)")
    logger.info(f"  성별비율: {filtered_df['male_ratio'].notna().sum()}편 ({filtered_df['male_ratio'].notna().sum()/len(filtered_df)*100:.1f}%)")

    # 저장
    filtered_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n💾 저장 완료: {output_path}")

    logger.info("\n" + "="*60)
    logger.info("✅ 필터링 완료!")
    logger.info("="*60)

    return filtered_df


if __name__ == '__main__':
    base_path = Path(__file__).parent.parent
    input_path = base_path / 'data' / 'processed' / 'final_analysis_dataset.csv'
    output_path = base_path / 'data' / 'processed' / 'final_analysis_dataset_2019_2024.csv'

    filter_new_releases(str(input_path), str(output_path))
