"""
영화 유형별 분류 및 분석 (상업영화 vs 독립영화)
- 매출액 기준으로 분류
- 유형별 성공 공식 분석
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FilmTypeAnalyzer:
    """영화 유형별 분석기"""

    # 분류 기준
    # 상업영화: 매출 60억원 이상
    # 독립영화: 매출 60억원 미만
    COMMERCIAL_THRESHOLD = 6_000_000_000  # 60억원

    def __init__(self, data_path: str):
        logger.info("데이터 로딩...")
        self.df = pd.read_csv(data_path)
        logger.info(f"  데이터: {len(self.df)}편")

    def classify_films(self):
        """영화 유형 분류"""
        logger.info("\n" + "="*60)
        logger.info("🎬 영화 유형 분류 (매출액 기준)")
        logger.info("="*60)

        df = self.df.copy()

        # 분류
        df['film_type'] = df['salesAcc'].apply(
            lambda x: 'commercial' if x >= self.COMMERCIAL_THRESHOLD else 'indie'
        )

        # 제작비 추정 (매출 * 0.495)
        df['estimated_production_cost'] = df['salesAcc'] * 0.495

        # 유형별 성공 기준
        # 상업영화: 매출 120억+ (제작비 30억 * 2배 회수 → 60.6억 * 2)
        # 독립영화: 매출 30억+ (제작비 15억 * 2배 회수)
        df['success_commercial'] = df['salesAcc'] >= 12_000_000_000  # 120억
        df['success_indie'] = df['salesAcc'] >= 3_000_000_000  # 30억

        df['success_by_type'] = df.apply(
            lambda row: row['success_commercial'] if row['film_type'] == 'commercial'
            else row['success_indie'],
            axis=1
        ).astype(int)

        self.df_classified = df

        # 통계
        commercial = df[df['film_type'] == 'commercial']
        indie = df[df['film_type'] == 'indie']

        logger.info(f"\n📊 분류 결과:")
        logger.info(f"  상업영화: {len(commercial)}편 ({len(commercial)/len(df)*100:.1f}%)")
        logger.info(f"  독립영화: {len(indie)}편 ({len(indie)/len(df)*100:.1f}%)")

        logger.info(f"\n💰 매출 통계:")
        logger.info(f"  상업영화 평균: {commercial['salesAcc'].mean()/1e8:.0f}억원")
        logger.info(f"  독립영화 평균: {indie['salesAcc'].mean()/1e8:.0f}억원")

        logger.info(f"\n👥 관객수 통계:")
        logger.info(f"  상업영화 평균: {commercial['audiAcc'].mean():,.0f}명")
        logger.info(f"  독립영화 평균: {indie['audiAcc'].mean():,.0f}명")

        logger.info(f"\n✅ 성공률:")
        logger.info(f"  상업영화: {commercial['success_by_type'].mean()*100:.1f}%")
        logger.info(f"  독립영화: {indie['success_by_type'].mean()*100:.1f}%")

        return df

    def analyze_by_type(self):
        """유형별 성공 공식 분석"""
        logger.info("\n" + "="*60)
        logger.info("📊 유형별 성공 공식 분석")
        logger.info("="*60)

        df = self.df_classified

        # 피처 준비
        df['openMonth'] = pd.to_datetime(df['openDt'], format='%Y%m%d', errors='coerce').dt.month

        results = {}

        for film_type in ['commercial', 'indie']:
            type_name = '상업영화' if film_type == 'commercial' else '독립영화'
            logger.info(f"\n{'='*60}")
            logger.info(f"🎯 {type_name} 분석")
            logger.info(f"{'='*60}")

            subset = df[df['film_type'] == film_type].copy()
            logger.info(f"  샘플 수: {len(subset)}편")
            logger.info(f"  성공: {subset['success_by_type'].sum()}편 ({subset['success_by_type'].mean()*100:.1f}%)")

            if len(subset) < 20:
                logger.warning(f"  ⚠️ 샘플 수 부족 - 분석 스킵")
                continue

            # 스타파워 상관관계
            logger.info(f"\n  📈 스타파워 상관관계:")
            corr_director = subset['director_star_power'].corr(subset['audiAcc'])
            corr_actor = subset['actor_star_power'].corr(subset['audiAcc'])
            corr_total = subset['total_star_power'].corr(subset['audiAcc'])

            logger.info(f"    감독: {corr_director:.3f}")
            logger.info(f"    배우: {corr_actor:.3f}")
            logger.info(f"    총합: {corr_total:.3f}")

            # 러닝타임 상관관계
            corr_runtime = subset['showTm'].corr(subset['audiAcc'])
            logger.info(f"    러닝타임: {corr_runtime:.3f}")

            # Random Forest 변수 중요도
            if subset['success_by_type'].sum() >= 5:  # 성공 샘플이 5개 이상
                logger.info(f"\n  🌲 Random Forest 변수 중요도:")

                # 피처 준비
                feature_cols = [
                    'director_star_power',
                    'actor_star_power',
                    'total_star_power',
                    'showTm',
                    'openMonth',
                    'year'
                ]

                subset_clean = subset[feature_cols + ['success_by_type']].dropna()

                if len(subset_clean) >= 20:
                    X = subset_clean[feature_cols]
                    y = subset_clean['success_by_type']

                    try:
                        # 분류 모델
                        clf = RandomForestClassifier(
                            n_estimators=100,
                            random_state=42,
                            max_depth=5,
                            min_samples_split=5
                        )
                        clf.fit(X, y)

                        importances = pd.DataFrame({
                            'feature': feature_cols,
                            'importance': clf.feature_importances_
                        }).sort_values('importance', ascending=False)

                        for idx, row in importances.head(5).iterrows():
                            logger.info(f"    {row['feature']:25s}: {row['importance']:.1%}")

                        results[film_type] = {
                            'importances': importances,
                            'correlations': {
                                'director': corr_director,
                                'actor': corr_actor,
                                'total': corr_total,
                                'runtime': corr_runtime
                            }
                        }
                    except Exception as e:
                        logger.warning(f"  ⚠️ 모델 학습 실패: {e}")

        return results

    def compare_types(self):
        """유형 간 비교 분석"""
        logger.info("\n" + "="*60)
        logger.info("🔍 상업영화 vs 독립영화 비교")
        logger.info("="*60)

        df = self.df_classified

        commercial = df[df['film_type'] == 'commercial']
        indie = df[df['film_type'] == 'indie']

        # 1. 스타파워 평균 비교
        logger.info("\n1. 스타파워 평균:")
        logger.info(f"  상업영화 - 감독: {commercial['director_star_power'].mean():.2f}, "
                   f"배우: {commercial['actor_star_power'].mean():.2f}, "
                   f"총합: {commercial['total_star_power'].mean():.2f}")
        logger.info(f"  독립영화 - 감독: {indie['director_star_power'].mean():.2f}, "
                   f"배우: {indie['actor_star_power'].mean():.2f}, "
                   f"총합: {indie['total_star_power'].mean():.2f}")

        # 2. 러닝타임 평균
        logger.info(f"\n2. 러닝타임 평균:")
        logger.info(f"  상업영화: {commercial['showTm'].mean():.0f}분")
        logger.info(f"  독립영화: {indie['showTm'].mean():.0f}분")

        # 3. 개봉 시즌 선호도
        logger.info(f"\n3. 주요 개봉 시즌:")

        commercial['season'] = commercial['openMonth'].apply(
            lambda x: '여름' if x in [6, 7, 8] else
            ('겨울' if x in [12, 1, 2] else
             ('봄' if x in [3, 4, 5] else '가을'))
        )

        indie['season'] = indie['openMonth'].apply(
            lambda x: '여름' if x in [6, 7, 8] else
            ('겨울' if x in [12, 1, 2] else
             ('봄' if x in [3, 4, 5] else '가을'))
        )

        logger.info(f"  상업영화 시즌 분포:")
        for season, count in commercial['season'].value_counts().head(3).items():
            logger.info(f"    {season}: {count}편 ({count/len(commercial)*100:.1f}%)")

        logger.info(f"  독립영화 시즌 분포:")
        for season, count in indie['season'].value_counts().head(3).items():
            logger.info(f"    {season}: {count}편 ({count/len(indie)*100:.1f}%)")

    def save_results(self, output_path: Path):
        """결과 저장"""
        logger.info(f"\n💾 결과 저장: {output_path}")

        self.df_classified.to_csv(output_path, index=False, encoding='utf-8-sig')

        logger.info(f"  저장 완료: {len(self.df_classified)}편")


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent

    data_path = base_path / 'data' / 'processed' / 'korean_movies_with_star_power.csv'
    output_path = base_path / 'data' / 'processed' / 'korean_movies_classified.csv'

    logger.info("\n" + "="*60)
    logger.info("🎬 영화 유형별 분류 및 분석")
    logger.info("="*60)
    logger.info(f"  입력: {data_path}")
    logger.info(f"  출력: {output_path}\n")

    # 분석
    analyzer = FilmTypeAnalyzer(str(data_path))
    analyzer.classify_films()
    analyzer.analyze_by_type()
    analyzer.compare_types()
    analyzer.save_results(output_path)

    logger.info("\n" + "="*60)
    logger.info("✅ 분석 완료!")
    logger.info("="*60)


if __name__ == '__main__':
    main()
