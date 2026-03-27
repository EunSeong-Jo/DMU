"""
최종 분석 데이터셋 생성
- KOBIS 데이터 + 네이버 평점 + 스타파워 통합
- 경쟁 강도, 계절, 성공 여부 등 파생 변수 생성
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FinalDatasetBuilder:
    """최종 분석 데이터셋 생성기"""

    def __init__(self, kobis_path: str, naver_path: str, star_power_path: str):
        """
        Args:
            kobis_path: KOBIS 병합 데이터
            naver_path: 네이버 평점 데이터
            star_power_path: 스타파워 계산 결과
        """
        self.kobis_df = pd.read_csv(kobis_path)
        self.naver_df = pd.read_csv(naver_path)
        self.star_power_df = pd.read_csv(star_power_path)

        logger.info(f"KOBIS 데이터: {len(self.kobis_df)}편")
        logger.info(f"네이버 데이터: {len(self.naver_df)}편")
        logger.info(f"스타파워 데이터: {len(self.star_power_df)}편")

    def merge_all_data(self) -> pd.DataFrame:
        """모든 데이터 병합"""
        logger.info("\n" + "="*60)
        logger.info("📊 데이터 병합 중...")
        logger.info("="*60)

        # KOBIS가 기준 (movieNm, openDt 포함)
        # 스타파워 데이터에서 중복 컬럼 제거
        star_power_cols = [col for col in self.star_power_df.columns
                          if col not in self.kobis_df.columns or col == 'movieCd']

        # KOBIS + 스타파워 병합 (movieCd 기준)
        merged = pd.merge(
            self.kobis_df,
            self.star_power_df[star_power_cols],
            on='movieCd',
            how='left'
        )

        # 네이버 평점 병합 (movie_name -> movieNm 매칭)
        naver_df_renamed = self.naver_df.rename(columns={'movie_name': 'movieNm'})

        # 관람객/네티즌 평점 중 관람객 평점만 사용
        naver_cols = ['movieNm', 'viewer_total', 'viewer_male', 'viewer_female',
                     'viewer_ratio_male', 'viewer_ratio_female',
                     'critic_rating_avg', 'critic_rating_count']

        naver_cols = [col for col in naver_cols if col in naver_df_renamed.columns]

        merged = pd.merge(
            merged,
            naver_df_renamed[naver_cols],
            on='movieNm',
            how='left'
        )

        # 간단한 컬럼명으로 변경
        merged = merged.rename(columns={
            'viewer_total': 'rating',
            'viewer_male': 'rating_male',
            'viewer_female': 'rating_female',
            'viewer_ratio_male': 'male_ratio',
            'viewer_ratio_female': 'female_ratio'
        })

        logger.info(f"✅ 병합 완료: {len(merged)}편")
        return merged

    def add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """파생 변수 추가"""
        logger.info("\n" + "="*60)
        logger.info("🔧 파생 변수 생성 중...")
        logger.info("="*60)

        result = df.copy()

        # 1. 개봉일 파싱
        result['openDt'] = pd.to_datetime(result['openDt'], errors='coerce')
        result['year'] = result['openDt'].dt.year
        result['month'] = result['openDt'].dt.month
        result['day_of_week'] = result['openDt'].dt.dayofweek  # 0=월요일

        # 2. 계절 분류
        def get_season(month):
            if pd.isna(month):
                return None
            if month in [3, 4, 5]:
                return '봄'
            elif month in [6, 7, 8]:
                return '여름'
            elif month in [9, 10, 11]:
                return '가을'
            else:
                return '겨울'

        result['season'] = result['month'].apply(get_season)

        # 3. 성공 여부 (300만명 기준)
        result['success'] = (result['audiAcc'] >= 3000000).astype(int)

        # 4. 성공 등급 (5단계)
        def get_success_grade(aud):
            if pd.isna(aud):
                return None
            if aud >= 10000000:
                return 'S급'  # 천만
            elif aud >= 5000000:
                return 'A급'  # 500만+
            elif aud >= 3000000:
                return 'B급'  # 300만+
            elif aud >= 1000000:
                return 'C급'  # 100만+
            else:
                return 'D급'  # 100만 미만

        result['success_grade'] = result['audiAcc'].apply(get_success_grade)

        # 5. 관람등급 정제
        def clean_watch_grade(grade):
            if pd.isna(grade):
                return 'Unknown'
            grade_str = str(grade)
            if '전체' in grade_str:
                return '전체관람가'
            elif '12' in grade_str:
                return '12세이상'
            elif '15' in grade_str:
                return '15세이상'
            elif '18' in grade_str or '청소년' in grade_str:
                return '청불'
            else:
                return 'Unknown'

        result['watch_grade_clean'] = result['watchGradeNm'].apply(clean_watch_grade)

        # 6. 상영시간 범주화
        def categorize_runtime(runtime):
            if pd.isna(runtime):
                return None
            try:
                runtime = float(runtime)
                if runtime < 90:
                    return '단편'
                elif runtime < 120:
                    return '표준'
                elif runtime < 150:
                    return '장편'
                else:
                    return '초장편'
            except:
                return None

        result['runtime_category'] = result['showTm'].apply(categorize_runtime)

        # 7. 장르 단순화 (첫 번째 장르만 사용)
        def get_main_genre(genres):
            if pd.isna(genres):
                return 'Unknown'
            genres_str = str(genres)
            if ',' in genres_str:
                return genres_str.split(',')[0].strip()
            return genres_str.strip()

        result['main_genre'] = result['genres'].apply(get_main_genre)

        # 8. 경쟁 강도 계산 (같은 주에 개봉한 영화 수)
        result['competition_count'] = 0
        for idx, row in result.iterrows():
            if pd.notna(row['openDt']):
                # 같은 주 (±3일)
                week_start = row['openDt'] - pd.Timedelta(days=3)
                week_end = row['openDt'] + pd.Timedelta(days=3)

                competition = result[
                    (result['openDt'] >= week_start) &
                    (result['openDt'] <= week_end) &
                    (result.index != idx)
                ]
                result.at[idx, 'competition_count'] = len(competition)

        # 9. 스타파워 등급
        def categorize_star_power(power):
            if pd.isna(power) or power == 0:
                return '신인'
            elif power < 500000:
                return '중견'
            elif power < 1500000:
                return '스타'
            else:
                return '슈퍼스타'

        result['director_power_grade'] = result['director_star_power'].apply(categorize_star_power)
        result['actor_power_grade'] = result['actor_star_power'].apply(categorize_star_power)

        # 10. 평점 등급
        def categorize_rating(rating):
            if pd.isna(rating):
                return None
            if rating >= 9.0:
                return '최상'
            elif rating >= 8.0:
                return '상'
            elif rating >= 7.0:
                return '중'
            else:
                return '하'

        result['rating_grade'] = result['rating'].apply(categorize_rating)

        logger.info("✅ 파생 변수 생성 완료:")
        logger.info(f"   - 시간 변수: year, month, season, day_of_week")
        logger.info(f"   - 성공 변수: success, success_grade")
        logger.info(f"   - 정제 변수: watch_grade_clean, main_genre, runtime_category")
        logger.info(f"   - 경쟁 변수: competition_count")
        logger.info(f"   - 등급 변수: director_power_grade, actor_power_grade, rating_grade")

        return result

    def generate_summary(self, df: pd.DataFrame):
        """데이터 요약 리포트"""
        logger.info("\n" + "="*60)
        logger.info("📈 최종 데이터셋 요약")
        logger.info("="*60)

        logger.info(f"\n총 영화 수: {len(df)}편")

        # 성공률
        success_rate = df['success'].mean() * 100
        logger.info(f"\n성공률 (300만+): {success_rate:.1f}%")

        # 성공 등급 분포
        logger.info(f"\n성공 등급 분포:")
        for grade in ['S급', 'A급', 'B급', 'C급', 'D급']:
            count = (df['success_grade'] == grade).sum()
            pct = count / len(df) * 100
            logger.info(f"  {grade}: {count}편 ({pct:.1f}%)")

        # 계절별 분포
        logger.info(f"\n계절별 영화 수:")
        season_counts = df['season'].value_counts()
        for season in ['봄', '여름', '가을', '겨울']:
            if season in season_counts:
                logger.info(f"  {season}: {season_counts[season]}편")

        # 장르별 분포
        logger.info(f"\n주요 장르 TOP 5:")
        top_genres = df['main_genre'].value_counts().head(5)
        for genre, count in top_genres.items():
            logger.info(f"  {genre}: {count}편")

        # 스타파워 분포
        logger.info(f"\n감독 스타파워 등급:")
        director_grades = df['director_power_grade'].value_counts()
        for grade in ['신인', '중견', '스타', '슈퍼스타']:
            if grade in director_grades:
                logger.info(f"  {grade}: {director_grades[grade]}편")

        # 데이터 완성도
        logger.info(f"\n데이터 완성도:")
        logger.info(f"  스타파워: {df['total_star_power'].notna().sum()}편 ({df['total_star_power'].notna().sum()/len(df)*100:.1f}%)")
        logger.info(f"  평점: {df['rating'].notna().sum()}편 ({df['rating'].notna().sum()/len(df)*100:.1f}%)")
        logger.info(f"  성별비율: {df['male_ratio'].notna().sum()}편 ({df['male_ratio'].notna().sum()/len(df)*100:.1f}%)")


def main():
    """메인 실행 함수"""

    # 경로 설정
    base_path = Path(__file__).parent.parent
    kobis_path = base_path / 'data' / 'raw' / 'kobis_merged.csv'
    naver_path = base_path / 'data' / 'raw' / 'naver_ratings.csv'
    star_power_path = base_path / 'data' / 'processed' / 'movies_with_star_power.csv'
    output_path = base_path / 'data' / 'processed' / 'final_analysis_dataset.csv'

    logger.info("="*60)
    logger.info("🎬 최종 분석 데이터셋 생성 시작")
    logger.info("="*60)
    logger.info(f"KOBIS: {kobis_path}")
    logger.info(f"네이버: {naver_path}")
    logger.info(f"스타파워: {star_power_path}")
    logger.info("="*60)

    # 데이터셋 빌더 초기화
    builder = FinalDatasetBuilder(
        kobis_path=str(kobis_path),
        naver_path=str(naver_path),
        star_power_path=str(star_power_path)
    )

    # 데이터 병합
    merged_df = builder.merge_all_data()

    # 파생 변수 추가
    final_df = builder.add_derived_features(merged_df)

    # 저장
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n💾 결과 저장: {output_path}")

    # 요약 리포트
    builder.generate_summary(final_df)

    logger.info("\n" + "="*60)
    logger.info("✅ 최종 데이터셋 생성 완료!")
    logger.info("="*60)
    logger.info(f"총 컬럼 수: {len(final_df.columns)}개")
    logger.info(f"총 영화 수: {len(final_df)}편")


if __name__ == '__main__':
    main()
