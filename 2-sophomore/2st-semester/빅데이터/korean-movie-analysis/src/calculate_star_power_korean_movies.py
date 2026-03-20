"""
스타파워 계산 (2014-2024 한국영화 220편)
- 역사 데이터: 2004-2024 전체 영화 (기존 kobis_merged.csv)
- 분석 대상: 2014-2024 한국영화 220편
- 개선된 스타파워 공식 적용
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class StarPowerCalculator:
    """스타파워 계산기 (개선된 공식)"""

    def __init__(self, historical_data_path: str):
        """
        Args:
            historical_data_path: 역사 데이터 경로 (2004-2024)
        """
        logger.info("역사 데이터 로딩...")
        self.historical_df = pd.read_csv(historical_data_path)

        # year 컬럼 생성 (openDt에서 추출)
        if 'year' not in self.historical_df.columns:
            # openDt 형식이 2003-12-24 또는 20031224일 수 있음
            self.historical_df['year'] = pd.to_datetime(self.historical_df['openDt'], errors='coerce').dt.year

        logger.info(f"  역사 데이터: {len(self.historical_df)}편 (2004-2024)")

        # 감독/배우별 영화 이력 구축
        self.director_filmography = defaultdict(list)
        self.actor_filmography = defaultdict(list)

        self._build_filmography()

    def _build_filmography(self):
        """감독/배우별 영화 이력 구축"""
        logger.info("감독/배우 이력 구축 중...")

        for _, row in self.historical_df.iterrows():
            year = row.get('year', row.get('prdtYear'))
            if pd.isna(year):
                continue

            year = int(year)
            aud = row.get('audiAcc', 0)

            movie_info = {
                'year': year,
                'audiAcc': aud,
                'movieNm': row.get('movieNm', '')
            }

            # 감독
            directors = str(row.get('directors', ''))
            if directors and directors != 'nan':
                for director in directors.split(','):
                    director = director.strip()
                    if director:
                        self.director_filmography[director].append(movie_info)

            # 배우 (상위 5명)
            actors = str(row.get('actors', ''))
            if actors and actors != 'nan':
                for actor in actors.split(',')[:5]:
                    actor = actor.strip()
                    if actor:
                        self.actor_filmography[actor].append(movie_info)

        logger.info(f"  감독: {len(self.director_filmography)}명")
        logger.info(f"  배우: {len(self.actor_filmography)}명")

    def calculate_person_star_power(self, person_name: str, target_year: int,
                                    filmography: dict) -> float:
        """
        개인 스타파워 계산 (개선된 공식)

        Args:
            person_name: 감독/배우 이름
            target_year: 분석 대상 영화 개봉 연도
            filmography: 영화 이력 딕셔너리

        Returns:
            스타파워 점수
        """
        if person_name not in filmography:
            return 0.0

        movies = filmography[person_name]

        # 대상 연도 이전 영화만 사용
        past_movies = [m for m in movies if m['year'] < target_year]

        if not past_movies:
            return 0.0

        # 관객수 리스트
        audiences = [m['audiAcc'] for m in past_movies]

        if not audiences:
            return 0.0

        # 기본 통계
        avg_aud = np.mean(audiences)
        std_aud = np.std(audiences) if len(audiences) > 1 else 0

        # 1. 시간 가중 평균 (50%)
        weighted_audiences = []
        weights = []
        for movie in past_movies:
            year_diff = target_year - movie['year']
            # 최근 영화일수록 높은 가중치
            time_weight = max(0.3, 1.0 - (year_diff * 0.04))  # 1년당 4% 감소
            weighted_audiences.append(movie['audiAcc'] * time_weight)
            weights.append(time_weight)

        time_weighted_avg = sum(weighted_audiences) / sum(weights)

        # 2. 안정성 계수 (20%) - 변동성이 낮을수록 높은 점수
        if avg_aud > 0:
            cv = std_aud / avg_aud  # 변동계수
            stability = max(0.5, 1.0 - min(cv, 0.5))
        else:
            stability = 0.5

        # 3. 성공률 (20%) - 300만 이상 영화 비율
        success_count = sum(1 for aud in audiences if aud >= 3_000_000)
        success_rate = success_count / len(audiences)

        # 4. 경험 보너스 (10%) - 작품 수 고려
        experience_bonus = min(1.0, 0.5 + (len(audiences) * 0.1))

        # 최종 스타파워 계산
        base_score = avg_aud / 1_000_000  # 백만 단위

        star_power = (
            time_weighted_avg / 1_000_000 * 0.5 +
            base_score * stability * 0.2 +
            base_score * success_rate * 0.2 +
            base_score * experience_bonus * 0.1
        )

        return star_power

    def calculate_movie_star_power(self, row: pd.Series) -> dict:
        """영화의 스타파워 계산"""
        year = int(row['year'])
        movie_name = row['movieNm']

        # 감독 스타파워
        directors = str(row.get('directors', ''))
        director_powers = []
        if directors and directors != 'nan':
            for director in directors.split(','):
                director = director.strip()
                if director:
                    power = self.calculate_person_star_power(
                        director, year, self.director_filmography
                    )
                    director_powers.append(power)

        director_star_power = max(director_powers) if director_powers else 0.0

        # 배우 스타파워 (상위 5명)
        actors = str(row.get('actors', ''))
        actor_powers = []
        if actors and actors != 'nan':
            for actor in actors.split(',')[:5]:
                actor = actor.strip()
                if actor:
                    power = self.calculate_person_star_power(
                        actor, year, self.actor_filmography
                    )
                    actor_powers.append(power)

        # 상위 3명 배우 평균
        if actor_powers:
            top_actors = sorted(actor_powers, reverse=True)[:3]
            actor_star_power = np.mean(top_actors)
        else:
            actor_star_power = 0.0

        # 총 스타파워 (감독 40% + 배우 60%)
        total_star_power = director_star_power * 0.4 + actor_star_power * 0.6

        return {
            'director_star_power': round(director_star_power, 2),
            'actor_star_power': round(actor_star_power, 2),
            'total_star_power': round(total_star_power, 2)
        }

    def calculate_all(self, analysis_data_path: str) -> pd.DataFrame:
        """전체 영화 스타파워 계산"""
        logger.info("\n" + "="*60)
        logger.info("🌟 스타파워 계산 시작")
        logger.info("="*60)

        # 분석 대상 데이터 로드
        analysis_df = pd.read_csv(analysis_data_path)
        logger.info(f"  분석 대상: {len(analysis_df)}편 (2014-2024 한국영화)")

        # 스타파워 계산
        star_powers = []
        for idx, row in analysis_df.iterrows():
            if (idx + 1) % 50 == 0:
                logger.info(f"  진행: {idx+1}/{len(analysis_df)}")

            sp = self.calculate_movie_star_power(row)
            star_powers.append(sp)

        # DataFrame에 추가
        result_df = analysis_df.copy()
        result_df['director_star_power'] = [sp['director_star_power'] for sp in star_powers]
        result_df['actor_star_power'] = [sp['actor_star_power'] for sp in star_powers]
        result_df['total_star_power'] = [sp['total_star_power'] for sp in star_powers]

        logger.info("\n" + "="*60)
        logger.info("✅ 스타파워 계산 완료")
        logger.info("="*60)

        # 통계
        logger.info(f"\n📊 스타파워 통계:")
        logger.info(f"  감독 평균: {result_df['director_star_power'].mean():.2f}")
        logger.info(f"  배우 평균: {result_df['actor_star_power'].mean():.2f}")
        logger.info(f"  총합 평균: {result_df['total_star_power'].mean():.2f}")

        # 관객수와의 상관관계
        corr_director = result_df['director_star_power'].corr(result_df['audiAcc'])
        corr_actor = result_df['actor_star_power'].corr(result_df['audiAcc'])
        corr_total = result_df['total_star_power'].corr(result_df['audiAcc'])

        logger.info(f"\n📈 관객수 상관관계:")
        logger.info(f"  감독: {corr_director:.3f}")
        logger.info(f"  배우: {corr_actor:.3f}")
        logger.info(f"  총합: {corr_total:.3f}")

        return result_df


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent

    # 역사 데이터 (2004-2024, 3548편)
    historical_path = base_path / 'data' / 'historical' / 'kobis_complete_2004_2024.csv'

    # 분석 대상 (2014-2024 한국영화 220편)
    analysis_path = base_path / 'data' / 'raw' / 'korean_movies_2014_2024_top20.csv'

    # 출력
    output_path = base_path / 'data' / 'processed' / 'korean_movies_with_star_power.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"\n📂 역사 데이터: {historical_path}")
    logger.info(f"📂 분석 대상: {analysis_path}")
    logger.info(f"📂 출력: {output_path}\n")

    # 계산
    calculator = StarPowerCalculator(str(historical_path))
    result_df = calculator.calculate_all(str(analysis_path))

    # 저장
    result_df.to_csv(output_path, index=False, encoding='utf-8-sig')

    logger.info(f"\n💾 저장 완료: {output_path}")
    logger.info(f"   {len(result_df)}편 데이터 (컬럼: {len(result_df.columns)}개)")


if __name__ == '__main__':
    main()
