"""
2014-2024년 한국영화 TOP 20 수집 (연간 박스오피스 사용)
- 더 빠르고 효율적인 방법
- KOBIS 연간 박스오피스 API 활용
"""

import requests
import pandas as pd
from pathlib import Path
import time
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()


class KoreanMovieYearlyCollector:
    """연간 박스오피스 기반 한국영화 수집기"""

    def __init__(self):
        self.api_key = os.getenv('KOBIS_API_KEY')
        if not self.api_key:
            raise ValueError("KOBIS_API_KEY가 .env 파일에 설정되지 않았습니다.")

        self.base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest"
        self.session = requests.Session()
        self.delay = 1.0

    def get_yearly_boxoffice(self, year: int) -> list:
        """연간 박스오피스 조회"""
        url = f"{self.base_url}/boxoffice/searchYearlyBoxOfficeList.json"
        params = {
            'key': self.api_key,
            'targetYear': str(year),
            'itemPerPage': 100  # 최대 100개
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            time.sleep(self.delay)

            if response.status_code == 200:
                data = response.json()
                return data.get('boxOfficeResult', {}).get('yearlyBoxOfficeList', [])
        except Exception as e:
            logger.error(f"  {year}년 박스오피스 조회 실패: {e}")

        return []

    def get_movie_detail(self, movie_cd: str) -> dict:
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
            logger.warning(f"  영화 {movie_cd} 상세정보 조회 실패: {e}")

        return {}

    def collect_year(self, year: int, target_count: int = 20) -> list:
        """특정 연도 한국영화 수집"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📅 {year}년 한국영화 TOP {target_count} 수집")
        logger.info(f"{'='*60}")

        # 연간 박스오피스 조회
        boxoffice_list = self.get_yearly_boxoffice(year)
        logger.info(f"  박스오피스 조회 결과: {len(boxoffice_list)}편")

        korean_movies = []

        for movie in boxoffice_list:
            if len(korean_movies) >= target_count:
                break

            movie_cd = movie.get('movieCd')
            movie_nm = movie.get('movieNm')

            # 영화 상세정보 조회
            detail = self.get_movie_detail(movie_cd)

            if not detail:
                continue

            # 국가 확인
            nations = detail.get('nations', [])
            nation_names = [n.get('nationNm') for n in nations]

            # 한국영화만 수집
            if '한국' in nation_names:
                movie_data = {
                    'movieCd': movie_cd,
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
                    'audiAcc': int(movie.get('audiAcc', 0)),
                    'salesAcc': int(movie.get('salesAcc', 0)),
                    'rank': int(movie.get('rank', 0)),
                    'year': year
                }

                korean_movies.append(movie_data)
                logger.info(f"  ✅ {len(korean_movies):2d}. {movie_data['movieNm']:30s} ({movie_data['audiAcc']:>10,d}명)")

        logger.info(f"\n  {year}년 한국영화 수집 완료: {len(korean_movies)}편")
        return korean_movies

    def collect_all_years(self, start_year: int = 2014, end_year: int = 2024,
                         movies_per_year: int = 20) -> pd.DataFrame:
        """전체 연도 수집"""
        logger.info("\n" + "="*60)
        logger.info(f"🎬 {start_year}-{end_year}년 한국영화 데이터 수집")
        logger.info(f"   목표: 연도별 TOP {movies_per_year}편")
        logger.info(f"   총 목표: {(end_year - start_year + 1) * movies_per_year}편")
        logger.info("="*60)

        all_movies = []

        for year in range(start_year, end_year + 1):
            yearly_movies = self.collect_year(year, movies_per_year)
            all_movies.extend(yearly_movies)

            logger.info(f"  누적: {len(all_movies)}편")

        # DataFrame 생성
        df = pd.DataFrame(all_movies)

        # 통계
        logger.info("\n" + "="*60)
        logger.info("📊 수집 완료 통계")
        logger.info("="*60)
        logger.info(f"  총 영화 수: {len(df)}편")
        logger.info(f"  평균 관객수: {df['audiAcc'].mean():,.0f}명")
        logger.info(f"  중앙값: {df['audiAcc'].median():,.0f}명")
        logger.info(f"  최대: {df['audiAcc'].max():,.0f}명 ({df.loc[df['audiAcc'].idxmax(), 'movieNm']})")
        logger.info(f"  최소: {df['audiAcc'].min():,.0f}명 ({df.loc[df['audiAcc'].idxmin(), 'movieNm']})")

        logger.info("\n  연도별 수집 현황:")
        yearly_counts = df['year'].value_counts().sort_index()
        for year, count in yearly_counts.items():
            avg_aud = df[df['year'] == year]['audiAcc'].mean()
            logger.info(f"    {int(year)}년: {count:2d}편 (평균 {avg_aud:,.0f}명)")

        return df


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent
    output_dir = base_path / 'data' / 'raw'
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("\n🚀 한국영화 데이터 수집 시작")
    logger.info("   2014-2024년 (11년)")
    logger.info("   연도별 TOP 20편")
    logger.info("   예상 소요 시간: 5-10분\n")

    # 수집기 초기화
    collector = KoreanMovieYearlyCollector()

    # 데이터 수집
    df = collector.collect_all_years(
        start_year=2014,
        end_year=2024,
        movies_per_year=20
    )

    # 저장
    output_path = output_dir / 'korean_movies_2014_2024_top20.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    logger.info(f"\n💾 저장 완료: {output_path}")
    logger.info(f"   총 {len(df)}편")

    logger.info("\n" + "="*60)
    logger.info("✅ 데이터 수집 완료!")
    logger.info("="*60)


if __name__ == '__main__':
    main()
