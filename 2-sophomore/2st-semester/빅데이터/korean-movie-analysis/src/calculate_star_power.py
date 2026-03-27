"""
스타파워 분석 스크립트
- 감독/배우의 과거 실적을 바탕으로 스타파워 점수 계산
- 2004-2018년 필모그래피 → 2019-2024년 영화의 스타파워 점수 부여
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Tuple

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StarPowerCalculator:
    """감독/배우 스타파워 계산기"""

    def __init__(self, historical_data_path: str, analysis_data_path: str):
        """
        Args:
            historical_data_path: 과거 데이터 경로 (2004-2024)
            analysis_data_path: 분석 대상 데이터 경로 (2019-2024)
        """
        self.historical_df = pd.read_csv(historical_data_path)
        self.analysis_df = pd.read_csv(analysis_data_path)

        # 날짜 정제
        self._clean_dates()

        logger.info(f"과거 데이터: {len(self.historical_df)}편")
        logger.info(f"분석 데이터: {len(self.analysis_df)}편")

    def _clean_dates(self):
        """날짜 필드 정제 및 연도 추출"""
        for df in [self.historical_df, self.analysis_df]:
            # openDt 정제
            df['openDt'] = df['openDt'].replace(r'^\s*$', np.nan, regex=True)

            # 연도 추출
            valid_dates = df['openDt'].notna()
            if valid_dates.sum() > 0:
                df.loc[valid_dates, 'year'] = pd.to_datetime(
                    df.loc[valid_dates, 'openDt'],
                    errors='coerce'
                ).dt.year

    def build_filmography(self) -> Tuple[Dict, Dict]:
        """
        과거 필모그래피 구축

        Returns:
            (director_filmography, actor_filmography)
        """
        logger.info("\n" + "="*60)
        logger.info("📚 필모그래피 구축 중...")
        logger.info("="*60)

        # 2019년 이전 데이터만 사용 (과거 실적)
        past_df = self.historical_df[
            (self.historical_df['year'] < 2019) &
            (self.historical_df['year'] >= 2004)
        ].copy()

        logger.info(f"과거 데이터 범위: 2004-2018년")
        logger.info(f"과거 영화 수: {len(past_df)}편")

        # 감독 필모그래피
        director_filmography = {}
        valid_directors = past_df[past_df['directors'].notna()]

        for _, row in valid_directors.iterrows():
            directors = str(row['directors']).split(',')
            audience = row.get('audiAcc', 0)

            # 숫자 변환 시도
            try:
                audience = float(audience) if pd.notna(audience) else 0
            except:
                audience = 0

            for director in directors:
                director = director.strip()
                if director and director != 'nan':
                    if director not in director_filmography:
                        director_filmography[director] = []
                    director_filmography[director].append({
                        'movieNm': row.get('movieNm', ''),
                        'year': row.get('year', 0),
                        'audiAcc': audience
                    })

        # 배우 필모그래피
        actor_filmography = {}
        valid_actors = past_df[past_df['actors'].notna()]

        for _, row in valid_actors.iterrows():
            actors = str(row['actors']).split(',')
            audience = row.get('audiAcc', 0)

            try:
                audience = float(audience) if pd.notna(audience) else 0
            except:
                audience = 0

            for actor in actors:
                actor = actor.strip()
                if actor and actor != 'nan':
                    if actor not in actor_filmography:
                        actor_filmography[actor] = []
                    actor_filmography[actor].append({
                        'movieNm': row.get('movieNm', ''),
                        'year': row.get('year', 0),
                        'audiAcc': audience
                    })

        logger.info(f"✅ 감독 수: {len(director_filmography)}명")
        logger.info(f"✅ 배우 수: {len(actor_filmography)}명")

        return director_filmography, actor_filmography

    def calculate_star_power(self, filmography: Dict, person_name: str) -> Dict:
        """
        개인 스타파워 계산

        Args:
            filmography: 전체 필모그래피 딕셔너리
            person_name: 감독/배우 이름

        Returns:
            스타파워 지표 딕셔너리
        """
        if person_name not in filmography:
            return {
                'past_movies_count': 0,
                'avg_audience': 0,
                'max_audience': 0,
                'total_audience': 0,
                'star_power_score': 0
            }

        movies = filmography[person_name]
        audiences = [m['audiAcc'] for m in movies if m['audiAcc'] > 0]

        if not audiences:
            return {
                'past_movies_count': len(movies),
                'avg_audience': 0,
                'max_audience': 0,
                'total_audience': 0,
                'star_power_score': 0
            }

        avg_aud = np.mean(audiences)
        max_aud = np.max(audiences)
        total_aud = np.sum(audiences)
        std_aud = np.std(audiences) if len(audiences) > 1 else 0

        # === 개선된 스타파워 계산 ===

        # 1. 기본 점수: 평균 관객수
        base_score = avg_aud

        # 2. 시간 가중치 (최근 영화일수록 높은 가중치)
        years = [m['year'] for m in movies if m['audiAcc'] > 0]
        if years:
            # 2019년 기준으로 시간 가중 평균 계산
            weighted_audiences = []
            weights = []
            for i, movie in enumerate(movies):
                if movie['audiAcc'] > 0 and movie['year'] > 0:
                    year_diff = 2019 - movie['year']  # 분석 시작년도
                    # 5년 이내: 1.0, 10년: 0.7, 15년: 0.4
                    time_weight = max(0.3, 1.0 - (year_diff * 0.04))
                    weighted_audiences.append(movie['audiAcc'] * time_weight)
                    weights.append(time_weight)

            if weighted_audiences:
                time_weighted_avg = sum(weighted_audiences) / sum(weights)
            else:
                time_weighted_avg = avg_aud
        else:
            time_weighted_avg = avg_aud

        # 3. 안정성 계수 (변동성이 낮을수록 신뢰도 높음)
        if len(audiences) > 1 and avg_aud > 0:
            # CV (변동계수) = 표준편차 / 평균
            cv = std_aud / avg_aud
            # 안정성: 변동이 클수록 패널티
            stability = max(0.5, 1.0 - min(cv, 0.5))
        else:
            stability = 0.8  # 영화 1편만 있으면 중간 신뢰도

        # 4. 성공률 (300만 이상 영화 비율)
        success_count = sum(1 for aud in audiences if aud >= 3000000)
        success_rate = success_count / len(audiences) if audiences else 0

        # 5. 경험치 보너스 (영화 수에 따른 가중치)
        experience_bonus = min(1.0, 0.5 + (len(audiences) * 0.1))

        # === 최종 스타파워 점수 ===
        # 시간가중평균(50%) + 안정성(20%) + 성공률(20%) + 경험치(10%)
        star_power = (
            time_weighted_avg * 0.5 +
            (base_score * stability) * 0.2 +
            (base_score * success_rate) * 0.2 +
            (base_score * experience_bonus) * 0.1
        )

        return {
            'past_movies_count': len(movies),
            'avg_audience': avg_aud,
            'max_audience': max_aud,
            'total_audience': total_aud,
            'std_audience': std_aud,
            'time_weighted_avg': time_weighted_avg,
            'stability': stability,
            'success_rate': success_rate,
            'star_power_score': star_power
        }

    def add_star_power_to_analysis_data(self,
                                       director_filmography: Dict,
                                       actor_filmography: Dict) -> pd.DataFrame:
        """
        분석 데이터에 스타파워 점수 추가

        Args:
            director_filmography: 감독 필모그래피
            actor_filmography: 배우 필모그래피

        Returns:
            스타파워가 추가된 데이터프레임
        """
        logger.info("\n" + "="*60)
        logger.info("⭐ 스타파워 점수 계산 중...")
        logger.info("="*60)

        result_df = self.analysis_df.copy()

        # 감독 스타파워
        director_power = []
        director_past_count = []
        director_avg_aud = []
        director_max_aud = []

        for _, row in result_df.iterrows():
            if pd.notna(row.get('directors')):
                directors = str(row['directors']).split(',')
                # 여러 감독 중 최대값 사용
                powers = [
                    self.calculate_star_power(director_filmography, d.strip())
                    for d in directors if d.strip()
                ]

                if powers:
                    max_power = max(powers, key=lambda x: x['star_power_score'])
                    director_power.append(max_power['star_power_score'])
                    director_past_count.append(max_power['past_movies_count'])
                    director_avg_aud.append(max_power['avg_audience'])
                    director_max_aud.append(max_power['max_audience'])
                else:
                    director_power.append(0)
                    director_past_count.append(0)
                    director_avg_aud.append(0)
                    director_max_aud.append(0)
            else:
                director_power.append(0)
                director_past_count.append(0)
                director_avg_aud.append(0)
                director_max_aud.append(0)

        result_df['director_star_power'] = director_power
        result_df['director_past_movies'] = director_past_count
        result_df['director_avg_audience'] = director_avg_aud
        result_df['director_max_audience'] = director_max_aud

        # 배우 스타파워
        actor_power = []
        actor_past_count = []
        actor_avg_aud = []
        actor_max_aud = []

        for _, row in result_df.iterrows():
            if pd.notna(row.get('actors')):
                actors = str(row['actors']).split(',')[:3]  # 주연 3명
                # 여러 배우 중 최대값 사용
                powers = [
                    self.calculate_star_power(actor_filmography, a.strip())
                    for a in actors if a.strip()
                ]

                if powers:
                    max_power = max(powers, key=lambda x: x['star_power_score'])
                    actor_power.append(max_power['star_power_score'])
                    actor_past_count.append(max_power['past_movies_count'])
                    actor_avg_aud.append(max_power['avg_audience'])
                    actor_max_aud.append(max_power['max_audience'])
                else:
                    actor_power.append(0)
                    actor_past_count.append(0)
                    actor_avg_aud.append(0)
                    actor_max_aud.append(0)
            else:
                actor_power.append(0)
                actor_past_count.append(0)
                actor_avg_aud.append(0)
                actor_max_aud.append(0)

        result_df['actor_star_power'] = actor_power
        result_df['actor_past_movies'] = actor_past_count
        result_df['actor_avg_audience'] = actor_avg_aud
        result_df['actor_max_audience'] = actor_max_aud

        # 통합 스타파워 (감독 60% + 배우 40%)
        result_df['total_star_power'] = (
            result_df['director_star_power'] * 0.6 +
            result_df['actor_star_power'] * 0.4
        )

        logger.info(f"✅ 스타파워 점수 계산 완료")
        logger.info(f"   - 감독 스타파워 평균: {result_df['director_star_power'].mean():.0f}")
        logger.info(f"   - 배우 스타파워 평균: {result_df['actor_star_power'].mean():.0f}")
        logger.info(f"   - 통합 스타파워 평균: {result_df['total_star_power'].mean():.0f}")

        return result_df

    def generate_report(self, result_df: pd.DataFrame):
        """스타파워 분석 리포트 생성"""
        logger.info("\n" + "="*60)
        logger.info("📊 스타파워 분석 리포트")
        logger.info("="*60)

        # 신인 vs 거장
        newcomer = result_df[result_df['director_past_movies'] == 0]
        veteran = result_df[result_df['director_past_movies'] >= 5]

        logger.info(f"\n👤 감독 경력별 분석:")
        logger.info(f"  신인 감독 ({len(newcomer)}편):")
        if len(newcomer) > 0:
            logger.info(f"    평균 관객수: {newcomer['audiAcc'].mean():.0f}명")
        logger.info(f"  베테랑 감독 ({len(veteran)}편, 5편 이상):")
        if len(veteran) > 0:
            logger.info(f"    평균 관객수: {veteran['audiAcc'].mean():.0f}명")

        # 상위 스타파워 TOP 10
        logger.info(f"\n⭐ 감독 스타파워 TOP 10:")
        top_directors = result_df.nlargest(10, 'director_star_power')[
            ['movieNm', 'directors', 'director_star_power', 'director_avg_audience', 'audiAcc']
        ]
        for idx, row in top_directors.iterrows():
            logger.info(f"  {row['movieNm'][:20]:20s} | {str(row['directors'])[:10]:10s} | "
                       f"스타파워: {row['director_star_power']:8.0f} | "
                       f"과거평균: {row['director_avg_audience']:8.0f} | "
                       f"실제: {row['audiAcc']:10.0f}")

        logger.info(f"\n⭐ 배우 스타파워 TOP 10:")
        top_actors = result_df.nlargest(10, 'actor_star_power')[
            ['movieNm', 'actors', 'actor_star_power', 'actor_avg_audience', 'audiAcc']
        ]
        for idx, row in top_actors.iterrows():
            actors_str = str(row['actors']).split(',')[0] if pd.notna(row['actors']) else 'N/A'
            logger.info(f"  {row['movieNm'][:20]:20s} | {actors_str[:10]:10s} | "
                       f"스타파워: {row['actor_star_power']:8.0f} | "
                       f"과거평균: {row['actor_avg_audience']:8.0f} | "
                       f"실제: {row['audiAcc']:10.0f}")

        # 상관관계 분석
        corr_director = result_df[['director_star_power', 'audiAcc']].corr().iloc[0, 1]
        corr_actor = result_df[['actor_star_power', 'audiAcc']].corr().iloc[0, 1]
        corr_total = result_df[['total_star_power', 'audiAcc']].corr().iloc[0, 1]

        logger.info(f"\n📈 스타파워-관객수 상관계수:")
        logger.info(f"  감독 스타파워: {corr_director:.3f}")
        logger.info(f"  배우 스타파워: {corr_actor:.3f}")
        logger.info(f"  통합 스타파워: {corr_total:.3f}")


def main():
    """메인 실행 함수"""

    # 경로 설정
    base_path = Path(__file__).parent.parent
    historical_path = base_path / 'data' / 'historical' / 'kobis_complete_2004_2024.csv'
    analysis_path = base_path / 'data' / 'raw' / 'kobis_merged.csv'  # 236편 분석 대상
    output_path = base_path / 'data' / 'processed' / 'movies_with_star_power.csv'

    logger.info("="*60)
    logger.info("🎬 스타파워 분석 시작")
    logger.info("="*60)
    logger.info(f"과거 데이터: {historical_path}")
    logger.info(f"분석 데이터: {analysis_path}")
    logger.info("="*60)

    # 계산기 초기화
    calculator = StarPowerCalculator(
        historical_data_path=str(historical_path),
        analysis_data_path=str(analysis_path)
    )

    # 필모그래피 구축
    director_filmography, actor_filmography = calculator.build_filmography()

    # 스타파워 계산
    result_df = calculator.add_star_power_to_analysis_data(
        director_filmography,
        actor_filmography
    )

    # 저장
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n💾 결과 저장: {output_path}")

    # 리포트 생성
    calculator.generate_report(result_df)

    logger.info("\n" + "="*60)
    logger.info("✅ 스타파워 분석 완료!")
    logger.info("="*60)


if __name__ == '__main__':
    main()
