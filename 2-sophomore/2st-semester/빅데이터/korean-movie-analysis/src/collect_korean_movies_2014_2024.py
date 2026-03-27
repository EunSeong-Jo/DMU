"""
2014-2024년 한국영화 TOP 20 데이터 수집
- 연도별 TOP 20 한국영화만 수집
- 11년 × 20편 = 220편 목표
- 외국영화 제외
"""

import requests
import pandas as pd
from pathlib import Path
import time
import logging
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# .env 파일 로드
load_dotenv()


class KoreanMovieCollector:
    """한국영화 데이터 수집기 (2014-2024)"""

    def __init__(self):
        self.api_key = os.getenv('KOBIS_API_KEY')
        if not self.api_key:
            raise ValueError("KOBIS_API_KEY가 .env 파일에 설정되지 않았습니다.")

        self.base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest"
        self.session = requests.Session()
        self.delay = 1.0  # API 호출 간격

    def get_yearly_korean_movies(self, year: int, target_count: int = 20) -> list:
        """연도별 한국영화 TOP 20 수집"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📅 {year}년 한국영화 TOP {target_count} 수집")
        logger.info(f"{'='*60}")

        korean_movies = []
        all_movies = []

        # 연도 전체 기간의 일별 박스오피스 수집
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        current_date = start_date
        movie_dict = {}  # 영화별 누적 관객수 추적

        while current_date <= end_date:
            date_str = current_date.strftime('%Y%m%d')

            try:
                # 일별 박스오피스 조회
                url = f"{self.base_url}/boxoffice/searchDailyBoxOfficeList.json"
                params = {
                    'key': self.api_key,
                    'targetDt': date_str
                }

                response = self.session.get(url, params=params, timeout=10)
                time.sleep(self.delay)

                if response.status_code == 200:
                    data = response.json()
                    daily_list = data.get('boxOfficeResult', {}).get('dailyBoxOfficeList', [])

                    for movie in daily_list:
                        movie_cd = movie.get('movieCd')
                        movie_nm = movie.get('movieNm')
                        audi_acc = int(movie.get('audiAcc', 0))

                        # 기존 영화보다 높은 관객수면 업데이트
                        if movie_cd not in movie_dict or movie_dict[movie_cd]['audiAcc'] < audi_acc:
                            movie_dict[movie_cd] = {
                                'movieCd': movie_cd,
                                'movieNm': movie_nm,
                                'audiAcc': audi_acc,
                                'rank': movie.get('rank')
                            }

            except Exception as e:
                logger.warning(f"  {date_str} 조회 실패: {e}")

            # 일주일씩 건너뛰기 (속도 향상)
            current_date += timedelta(days=7)

        # 관객수 기준 정렬
        sorted_movies = sorted(movie_dict.values(), key=lambda x: x['audiAcc'], reverse=True)

        logger.info(f"  총 {len(sorted_movies)}편 발견")

        # 각 영화의 상세정보 조회하여 한국영화만 필터링
        for movie in sorted_movies:
            if len(korean_movies) >= target_count:
                break

            try:
                # 영화 상세정보 조회
                url = f"{self.base_url}/movie/searchMovieInfo.json"
                params = {
                    'key': self.api_key,
                    'movieCd': movie['movieCd']
                }

                response = self.session.get(url, params=params, timeout=10)
                time.sleep(self.delay)

                if response.status_code == 200:
                    data = response.json()
                    movie_info = data.get('movieInfoResult', {}).get('movieInfo', {})

                    # 국가 확인
                    nations = movie_info.get('nations', [])
                    nation_names = [n.get('nationNm') for n in nations]

                    # 한국영화만 수집
                    if '한국' in nation_names:
                        movie_detail = {
                            'movieCd': movie['movieCd'],
                            'movieNm': movie_info.get('movieNm'),
                            'movieNmEn': movie_info.get('movieNmEn'),
                            'prdtYear': movie_info.get('prdtYear'),
                            'openDt': movie_info.get('openDt'),
                            'showTm': movie_info.get('showTm'),
                            'genres': ','.join([g.get('genreNm') for g in movie_info.get('genres', [])]),
                            'directors': ','.join([d.get('peopleNm') for d in movie_info.get('directors', [])]),
                            'actors': ','.join([a.get('peopleNm') for a in movie_info.get('actors', [])[:5]]),
                            'nations': ','.join(nation_names),
                            'watchGradeNm': ','.join([w.get('watchGradeNm') for w in movie_info.get('audits', [])]),
                            'typeNm': movie_info.get('typeNm'),
                            'audiAcc': movie['audiAcc'],
                            'year': year
                        }

                        korean_movies.append(movie_detail)
                        logger.info(f"  ✅ {len(korean_movies):2d}. {movie_detail['movieNm']:30s} ({movie['audiAcc']:>10,d}명)")

            except Exception as e:
                logger.warning(f"  영화 {movie['movieNm']} 상세정보 조회 실패: {e}")

        logger.info(f"\n  한국영화 수집 완료: {len(korean_movies)}편")
        return korean_movies

    def collect_all_years(self, start_year: int = 2014, end_year: int = 2024,
                         movies_per_year: int = 20) -> pd.DataFrame:
        """전체 연도 데이터 수집"""
        logger.info("\n" + "="*60)
        logger.info(f"🎬 {start_year}-{end_year}년 한국영화 데이터 수집 시작")
        logger.info(f"   목표: 연도별 TOP {movies_per_year}편")
        logger.info(f"   총 목표: {(end_year - start_year + 1) * movies_per_year}편")
        logger.info("="*60)

        all_movies = []

        for year in range(start_year, end_year + 1):
            yearly_movies = self.get_yearly_korean_movies(year, movies_per_year)
            all_movies.extend(yearly_movies)

            logger.info(f"  {year}년 누적: {len(all_movies)}편")

        # DataFrame 생성
        df = pd.DataFrame(all_movies)

        logger.info("\n" + "="*60)
        logger.info(f"✅ 전체 수집 완료: {len(df)}편")
        logger.info("="*60)

        # 통계
        logger.info("\n📊 수집 통계:")
        logger.info(f"  총 영화 수: {len(df)}편")
        logger.info(f"  평균 관객수: {df['audiAcc'].mean():,.0f}명")
        logger.info(f"  최대 관객수: {df['audiAcc'].max():,.0f}명 ({df.loc[df['audiAcc'].idxmax(), 'movieNm']})")
        logger.info(f"  최소 관객수: {df['audiAcc'].min():,.0f}명 ({df.loc[df['audiAcc'].idxmin(), 'movieNm']})")

        logger.info("\n  연도별 수집 현황:")
        yearly_counts = df['year'].value_counts().sort_index()
        for year, count in yearly_counts.items():
            logger.info(f"    {int(year)}년: {count}편")

        return df


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent
    output_dir = base_path / 'data' / 'raw'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 수집기 초기화
    collector = KoreanMovieCollector()

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
    logger.info(f"   총 {len(df)}편 수집됨")


if __name__ == '__main__':
    main()
