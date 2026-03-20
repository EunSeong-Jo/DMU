"""
2014-2024년 한국영화 TOP 20 수집
- 주간 박스오피스 방식 사용
- 한국영화만 필터링
- 연도별 누적 관객수 기준 TOP 20
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import logging
import time
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class KoreanTop20Collector:
    """한국영화 TOP 20 수집기"""

    def __init__(self):
        self.api_key = os.getenv('KOBIS_API_KEY')
        if not self.api_key:
            raise ValueError("KOBIS_API_KEY가 .env 파일에 설정되지 않았습니다.")

        self.base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest"
        self.session = requests.Session()
        self.delay = 0.5  # 속도 향상

    def get_weekly_boxoffice(self, target_date: str):
        """주간 박스오피스 조회"""
        url = f"{self.base_url}/boxoffice/searchWeeklyBoxOfficeList.json"
        params = {
            'key': self.api_key,
            'targetDt': target_date,
            'weekGb': '0'
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            time.sleep(self.delay)

            if response.status_code == 200:
                data = response.json()
                return data.get('boxOfficeResult', {}).get('weeklyBoxOfficeList', [])
        except Exception as e:
            logger.warning(f"  {target_date} 조회 실패: {e}")

        return []

    def get_movie_detail(self, movie_cd: str):
        """영화 상세정보 조회"""
        url = f"{self.base_url}/movie/searchMovieInfo.json"
        params = {
            'key': self.api_key,
            'movieCd': movie_cd
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            time.sleep(self.delay)

            if response.status_code == 200:
                data = response.json()
                return data.get('movieInfoResult', {}).get('movieInfo', {})
        except Exception as e:
            logger.warning(f"  영화 {movie_cd} 조회 실패: {e}")

        return {}

    def collect_year(self, year: int) -> list:
        """특정 연도 한국영화 수집"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📅 {year}년 한국영화 수집 중...")
        logger.info(f"{'='*60}")

        # 영화별 최대 관객수 추적
        movie_dict = {}

        # 매월 첫째 주 일요일 조회 (12번)
        for month in range(1, 13):
            # 해당 월의 첫째 주 일요일 찾기
            first_day = datetime(year, month, 1)
            days_until_sunday = (6 - first_day.weekday()) % 7
            if days_until_sunday == 0 and first_day.weekday() != 6:
                days_until_sunday = 7
            first_sunday = first_day + timedelta(days=days_until_sunday)

            target_date = first_sunday.strftime('%Y%m%d')

            # 주간 박스오피스 조회
            boxoffice = self.get_weekly_boxoffice(target_date)

            for movie in boxoffice:
                movie_cd = movie.get('movieCd')
                audi_acc = int(movie.get('audiAcc', 0))

                # 최대 관객수 업데이트
                if movie_cd not in movie_dict or movie_dict[movie_cd]['audiAcc'] < audi_acc:
                    movie_dict[movie_cd] = {
                        'movieCd': movie_cd,
                        'movieNm': movie.get('movieNm'),
                        'audiAcc': audi_acc,
                        'salesAcc': int(movie.get('salesAcc', 0))
                    }

        logger.info(f"  월별 박스오피스 조회 완료: {len(movie_dict)}편 발견")

        # 관객수 기준 정렬
        sorted_movies = sorted(movie_dict.values(), key=lambda x: x['audiAcc'], reverse=True)

        # 상세정보 조회 (한국영화 20편 수집)
        korean_movies = []

        for movie in sorted_movies:
            if len(korean_movies) >= 20:
                break

            detail = self.get_movie_detail(movie['movieCd'])

            if not detail:
                continue

            # 국가 확인
            nations = detail.get('nations', [])
            nation_names = [n.get('nationNm') for n in nations]

            # 한국영화만
            if '한국' in nation_names:
                movie_data = {
                    'movieCd': movie['movieCd'],
                    'movieNm': detail.get('movieNm'),
                    'movieNmEn': detail.get('movieNmEn'),
                    'prdtYear': detail.get('prdtYear'),
                    'openDt': detail.get('openDt'),
                    'showTm': detail.get('showTm'),
                    'genres': ','.join([g.get('genreNm') for g in detail.get('genres', [])]),
                    'directors': ','.join([d.get('peopleNm') for d in detail.get('directors', [])]),
                    'actors': ','.join([a.get('peopleNm') for a in detail.get('actors', [])[:5]]),
                    'nations': ','.join(nation_names),
                    'watchGradeNm': ','.join([w.get('watchGradeNm') for w in detail.get('audits', [])]),
                    'typeNm': detail.get('typeNm'),
                    'audiAcc': movie['audiAcc'],
                    'salesAcc': movie['salesAcc'],
                    'year': year
                }

                korean_movies.append(movie_data)
                logger.info(f"  ✅ {len(korean_movies):2d}. {movie_data['movieNm']:25s} ({movie_data['audiAcc']:>10,d}명)")

        logger.info(f"\n  {year}년 한국영화 수집 완료: {len(korean_movies)}편")
        return korean_movies

    def collect_all(self, start_year=2014, end_year=2024) -> pd.DataFrame:
        """전체 연도 수집"""
        logger.info("\n" + "="*60)
        logger.info("🎬 2014-2024년 한국영화 TOP 20 수집")
        logger.info(f"   목표: 11년 × 20편 = 220편")
        logger.info(f"   예상 시간: 10-15분")
        logger.info("="*60)

        all_movies = []

        for year in range(start_year, end_year + 1):
            yearly_movies = self.collect_year(year)
            all_movies.extend(yearly_movies)

            logger.info(f"\n  📊 누적: {len(all_movies)}편")

        # DataFrame 생성
        df = pd.DataFrame(all_movies)

        logger.info("\n" + "="*60)
        logger.info("✅ 수집 완료!")
        logger.info("="*60)
        logger.info(f"  총 수집: {len(df)}편")
        logger.info(f"  평균 관객수: {df['audiAcc'].mean():,.0f}명")
        logger.info(f"  중앙값: {df['audiAcc'].median():,.0f}명")

        logger.info("\n  연도별 수집 현황:")
        for year in range(start_year, end_year + 1):
            year_df = df[df['year'] == year]
            logger.info(f"    {year}년: {len(year_df):2d}편 (평균 {year_df['audiAcc'].mean():,.0f}명)")

        return df


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent
    output_dir = base_path / 'data' / 'raw'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 수집
    collector = KoreanTop20Collector()
    df = collector.collect_all(2014, 2024)

    # 저장
    output_path = output_dir / 'korean_movies_2014_2024_top20.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    logger.info(f"\n💾 저장: {output_path}")
    logger.info(f"   {len(df)}편 수집 완료")


if __name__ == '__main__':
    main()
