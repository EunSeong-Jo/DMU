"""
상업영화와 독립영화 분류 및 데이터셋 생성
- 제작비 30억 기준 (매출액 60.6억 역산)
- 상업영화: 70편
- 독립영화: 184편
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FilmTypeClassifier:
    """영화 타입 분류기 (상업/독립)"""

    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)
        logger.info(f"데이터 로드: {len(self.df)}편")

        # 제작비 30억 기준 매출액 역산
        # 제작사 수익 = 매출 × 49.5%
        # 제작비 30억 회수 = 매출 60.6억
        self.COMMERCIAL_THRESHOLD = 6_060_000_000  # 60.6억

    def classify_films(self):
        """영화 분류"""
        logger.info("\n" + "="*60)
        logger.info("🎬 영화 타입 분류")
        logger.info("="*60)

        # 제작사 예상 수익 계산
        self.df['producer_revenue'] = self.df['salesAcc'] * 0.495

        # 영화 타입 분류
        self.df['film_type'] = self.df['salesAcc'].apply(
            lambda x: 'commercial' if x >= self.COMMERCIAL_THRESHOLD else 'indie'
        )

        # 통계
        commercial_count = (self.df['film_type'] == 'commercial').sum()
        indie_count = (self.df['film_type'] == 'indie').sum()

        logger.info(f"\n분류 기준: 매출액 {self.COMMERCIAL_THRESHOLD/100000000:.1f}억원")
        logger.info(f"(제작비 30억 회수 기준)")
        logger.info(f"\n상업영화: {commercial_count}편 ({commercial_count/len(self.df)*100:.1f}%)")
        logger.info(f"독립/저예산 영화: {indie_count}편 ({indie_count/len(self.df)*100:.1f}%)")

        return self.df

    def analyze_by_type(self):
        """타입별 통계 분석"""
        logger.info("\n" + "="*60)
        logger.info("📊 영화 타입별 통계")
        logger.info("="*60)

        for film_type in ['commercial', 'indie']:
            type_name = "상업영화" if film_type == 'commercial' else "독립/저예산 영화"
            subset = self.df[self.df['film_type'] == film_type]

            logger.info(f"\n{'='*40}")
            logger.info(f"🎥 {type_name} ({len(subset)}편)")
            logger.info(f"{'='*40}")

            # 기본 통계
            logger.info(f"\n📈 관객수 통계:")
            logger.info(f"  평균: {subset['audiAcc'].mean():>15,.0f}명")
            logger.info(f"  중앙값: {subset['audiAcc'].median():>13,.0f}명")
            logger.info(f"  최대: {subset['audiAcc'].max():>15,.0f}명")
            logger.info(f"  최소: {subset['audiAcc'].min():>15,.0f}명")

            logger.info(f"\n💰 매출액 통계:")
            logger.info(f"  평균: {subset['salesAcc'].mean()/100000000:>15.1f}억원")
            logger.info(f"  중앙값: {subset['salesAcc'].median()/100000000:>13.1f}억원")

            logger.info(f"\n🏢 제작사 예상 수익:")
            logger.info(f"  평균: {subset['producer_revenue'].mean()/100000000:>15.1f}억원")
            logger.info(f"  중앙값: {subset['producer_revenue'].median()/100000000:>13.1f}억원")

            # 스타파워
            if 'total_star_power' in subset.columns:
                logger.info(f"\n⭐ 스타파워 통계:")
                logger.info(f"  평균 통합 스타파워: {subset['total_star_power'].mean():>10,.0f}")
                logger.info(f"  평균 배우 스타파워: {subset['actor_star_power'].mean():>10,.0f}")
                logger.info(f"  평균 감독 스타파워: {subset['director_star_power'].mean():>10,.0f}")

            # 평점
            if 'rating' in subset.columns:
                rating_available = subset['rating'].notna().sum()
                logger.info(f"\n📝 평점 통계 ({rating_available}편):")
                logger.info(f"  평균 평점: {subset['rating'].mean():>10.2f}")

            # 장르 분포
            if 'main_genre' in subset.columns:
                logger.info(f"\n🎭 주요 장르 TOP 5:")
                genre_counts = subset['main_genre'].value_counts().head(5)
                for genre, count in genre_counts.items():
                    logger.info(f"  {genre:15s}: {count:>3}편 ({count/len(subset)*100:>5.1f}%)")

    def set_success_criteria(self):
        """타입별 성공 기준 설정"""
        logger.info("\n" + "="*60)
        logger.info("🎯 타입별 성공 기준 설정")
        logger.info("="*60)

        # 상업영화: 매출 120억 이상 (제작비 2배 회수)
        commercial_threshold = 12_000_000_000
        self.df.loc[self.df['film_type'] == 'commercial', 'success_new'] = \
            (self.df.loc[self.df['film_type'] == 'commercial', 'salesAcc'] >= commercial_threshold).astype(int)

        # 독립영화: 매출 30억 이상 (제작비 15억 회수, 손익분기점)
        indie_threshold = 3_000_000_000
        self.df.loc[self.df['film_type'] == 'indie', 'success_new'] = \
            (self.df.loc[self.df['film_type'] == 'indie', 'salesAcc'] >= indie_threshold).astype(int)

        logger.info(f"\n상업영화 성공 기준: 매출 {commercial_threshold/100000000:.0f}억원 이상")
        logger.info(f"  (제작비 평균 60억 × 2배 회수)")
        commercial = self.df[self.df['film_type'] == 'commercial']
        success_count = commercial['success_new'].sum()
        logger.info(f"  성공: {success_count}편 ({success_count/len(commercial)*100:.1f}%)")
        logger.info(f"  실패: {len(commercial)-success_count}편 ({(len(commercial)-success_count)/len(commercial)*100:.1f}%)")

        logger.info(f"\n독립영화 성공 기준: 매출 {indie_threshold/100000000:.0f}억원 이상")
        logger.info(f"  (제작비 평균 15억 × 2배 회수)")
        indie = self.df[self.df['film_type'] == 'indie']
        success_count = indie['success_new'].sum()
        logger.info(f"  성공: {success_count}편 ({success_count/len(indie)*100:.1f}%)")
        logger.info(f"  실패: {len(indie)-success_count}편 ({(len(indie)-success_count)/len(indie)*100:.1f}%)")

        return self.df

    def save_datasets(self, output_dir: str):
        """타입별 데이터셋 저장"""
        logger.info("\n" + "="*60)
        logger.info("💾 데이터셋 저장")
        logger.info("="*60)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 전체 데이터 (film_type, success_new 컬럼 추가)
        full_path = output_path / 'final_dataset_with_types.csv'
        self.df.to_csv(full_path, index=False, encoding='utf-8-sig')
        logger.info(f"✅ 전체 데이터 저장: {full_path}")
        logger.info(f"   총 {len(self.df)}편 (film_type, success_new 컬럼 추가)")

        # 상업영화만
        commercial_df = self.df[self.df['film_type'] == 'commercial']
        commercial_path = output_path / 'commercial_films.csv'
        commercial_df.to_csv(commercial_path, index=False, encoding='utf-8-sig')
        logger.info(f"✅ 상업영화 데이터 저장: {commercial_path}")
        logger.info(f"   총 {len(commercial_df)}편")

        # 독립영화만
        indie_df = self.df[self.df['film_type'] == 'indie']
        indie_path = output_path / 'indie_films.csv'
        indie_df.to_csv(indie_path, index=False, encoding='utf-8-sig')
        logger.info(f"✅ 독립영화 데이터 저장: {indie_path}")
        logger.info(f"   총 {len(indie_df)}편")


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent
    data_path = base_path / 'data' / 'processed' / 'final_analysis_dataset_2019_2024.csv'
    output_dir = base_path / 'data' / 'processed'

    logger.info("="*60)
    logger.info("🎬 상업/독립 영화 분류 시작")
    logger.info("="*60)

    # 분류기 초기화
    classifier = FilmTypeClassifier(str(data_path))

    # 영화 분류
    classifier.classify_films()

    # 타입별 통계 분석
    classifier.analyze_by_type()

    # 성공 기준 설정
    classifier.set_success_criteria()

    # 데이터셋 저장
    classifier.save_datasets(str(output_dir))

    logger.info("\n" + "="*60)
    logger.info("✅ 분류 완료!")
    logger.info("="*60)


if __name__ == '__main__':
    main()
