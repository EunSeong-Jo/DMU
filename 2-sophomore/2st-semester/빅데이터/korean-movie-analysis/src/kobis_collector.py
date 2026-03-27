"""
KOBIS (영화진흥위원회) Open API 데이터 수집 모듈

주요 기능:
1. 일별 박스오피스 데이터 수집
2. 영화 상세정보 수집
3. 데이터 병합 및 저장
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import json
import logging
from tqdm import tqdm

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KOBISCollector:
    """KOBIS API 데이터 수집 클래스"""

    BASE_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest"

    def __init__(self, api_key: str, delay: float = 1.0):
        """
        Args:
            api_key: KOBIS API 키
            delay: API 호출 간 대기 시간 (초)
        """
        self.api_key = api_key
        self.delay = delay
        self.session = requests.Session()

    def get_daily_boxoffice(self, target_date: str) -> Optional[Dict]:
        """
        일별 박스오피스 데이터 조회

        Args:
            target_date: 조회 날짜 (YYYYMMDD)

        Returns:
            박스오피스 데이터 또는 None
        """
        url = f"{self.BASE_URL}/boxoffice/searchDailyBoxOfficeList.json"
        params = {
            "key": self.api_key,
            "targetDt": target_date
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # API 응답 확인
            if 'boxOfficeResult' in data:
                time.sleep(self.delay)  # API 호출 제한 준수
                return data['boxOfficeResult']
            else:
                logger.warning(f"No data for {target_date}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"API 호출 실패 ({target_date}): {e}")
            return None

    def get_movie_info(self, movie_code: str) -> Optional[Dict]:
        """
        영화 상세정보 조회

        Args:
            movie_code: 영화 코드

        Returns:
            영화 상세정보 또는 None
        """
        url = f"{self.BASE_URL}/movie/searchMovieInfo.json"
        params = {
            "key": self.api_key,
            "movieCd": movie_code
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'movieInfoResult' in data and 'movieInfo' in data['movieInfoResult']:
                time.sleep(self.delay)
                return data['movieInfoResult']['movieInfo']
            else:
                logger.warning(f"No movie info for {movie_code}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"영화정보 조회 실패 ({movie_code}): {e}")
            return None

    def collect_boxoffice_period(
        self,
        start_date: datetime,
        end_date: datetime,
        sample_interval: int = 7
    ) -> pd.DataFrame:
        """
        기간별 박스오피스 데이터 수집

        Args:
            start_date: 시작일
            end_date: 종료일
            sample_interval: 샘플링 간격 (일)

        Returns:
            박스오피스 데이터프레임
        """
        logger.info(f"박스오피스 수집 시작: {start_date.date()} ~ {end_date.date()}")

        movie_dict = {}  # 영화코드: 영화정보
        current_date = start_date

        # 날짜별 박스오피스 수집
        dates = []
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=sample_interval)

        for date in tqdm(dates, desc="박스오피스 수집"):
            target_dt = date.strftime("%Y%m%d")
            result = self.get_daily_boxoffice(target_dt)

            if result and 'dailyBoxOfficeList' in result:
                for movie in result['dailyBoxOfficeList']:
                    movie_code = movie.get('movieCd')

                    if movie_code and movie_code not in movie_dict:
                        # 영화 기본정보 저장
                        movie_dict[movie_code] = {
                            'movieCd': movie_code,
                            'movieNm': movie.get('movieNm'),
                            'openDt': movie.get('openDt'),
                            'audiAcc': int(movie.get('audiAcc', 0)),  # 누적관객수
                            'salesAcc': int(movie.get('salesAcc', 0)),  # 누적매출액
                            'rank': int(movie.get('rank', 0)),
                            'rankOldAndNew': movie.get('rankOldAndNew')
                        }

        logger.info(f"총 {len(movie_dict)}편의 영화 수집 완료")

        # 데이터프레임 변환
        df = pd.DataFrame.from_dict(movie_dict, orient='index')
        df = df.sort_values('audiAcc', ascending=False)

        return df

    def collect_movie_details(self, movie_codes: List[str]) -> pd.DataFrame:
        """
        영화 상세정보 일괄 수집

        Args:
            movie_codes: 영화 코드 리스트

        Returns:
            영화 상세정보 데이터프레임
        """
        logger.info(f"영화 상세정보 수집 시작: {len(movie_codes)}편")

        details = []

        for movie_code in tqdm(movie_codes, desc="상세정보 수집"):
            info = self.get_movie_info(movie_code)

            if info:
                # 장르 추출
                genres = [g['genreNm'] for g in info.get('genres', [])]
                genre_str = ','.join(genres) if genres else '기타'

                # 감독 추출
                directors = [d['peopleNm'] for d in info.get('directors', [])]
                director_str = ','.join(directors) if directors else '정보없음'

                # 배우 추출 (주연 3명)
                actors = [a['peopleNm'] for a in info.get('actors', [])[:3]]
                actor_str = ','.join(actors) if actors else '정보없음'

                # 제작국가
                nations = [n['nationNm'] for n in info.get('nations', [])]
                nation_str = ','.join(nations) if nations else '한국'

                details.append({
                    'movieCd': movie_code,
                    'movieNm': info.get('movieNm'),
                    'movieNmEn': info.get('movieNmEn', ''),
                    'prdtYear': info.get('prdtYear'),
                    'showTm': info.get('showTm'),  # 상영시간
                    'openDt': info.get('openDt'),
                    'genres': genre_str,
                    'directors': director_str,
                    'actors': actor_str,
                    'nations': nation_str,
                    'watchGradeNm': info.get('audits', [{}])[0].get('watchGradeNm', '정보없음') if info.get('audits') else '정보없음',
                    'typeNm': info.get('typeNm', '장편')
                })

        logger.info(f"상세정보 수집 완료: {len(details)}편")

        df = pd.DataFrame(details)
        return df

    def save_data(self, df: pd.DataFrame, filepath: str):
        """데이터프레임 저장"""
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        logger.info(f"데이터 저장 완료: {filepath}")


def main():
    """메인 실행 함수"""
    import os
    from dotenv import load_dotenv

    # 환경변수 로드
    load_dotenv()
    API_KEY = os.getenv('KOBIS_API_KEY')

    if not API_KEY:
        logger.error("KOBIS_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        return

    # 수집 설정
    START_DATE = datetime(2019, 1, 1)
    END_DATE = datetime(2024, 12, 31)

    # 수집기 초기화
    collector = KOBISCollector(api_key=API_KEY, delay=1.0)

    # 1단계: 박스오피스 데이터 수집
    logger.info("=" * 60)
    logger.info("1단계: 박스오피스 데이터 수집")
    logger.info("=" * 60)

    boxoffice_df = collector.collect_boxoffice_period(
        start_date=START_DATE,
        end_date=END_DATE,
        sample_interval=7  # 주간 샘플링
    )

    # 상위 300편 선택 (관객수 기준)
    top_movies = boxoffice_df.head(300)

    # 저장
    os.makedirs('../data/raw', exist_ok=True)
    collector.save_data(top_movies, '../data/raw/kobis_boxoffice.csv')

    # 2단계: 영화 상세정보 수집
    logger.info("=" * 60)
    logger.info("2단계: 영화 상세정보 수집")
    logger.info("=" * 60)

    movie_codes = top_movies['movieCd'].tolist()
    details_df = collector.collect_movie_details(movie_codes)

    # 저장
    collector.save_data(details_df, '../data/raw/kobis_movie_details.csv')

    # 3단계: 데이터 병합
    logger.info("=" * 60)
    logger.info("3단계: 데이터 병합")
    logger.info("=" * 60)

    merged_df = pd.merge(
        boxoffice_df,
        details_df,
        on='movieCd',
        how='left',
        suffixes=('_box', '_detail')
    )

    # 중복 컬럼 정리
    if 'movieNm_detail' in merged_df.columns:
        merged_df['movieNm'] = merged_df['movieNm_detail'].fillna(merged_df['movieNm_box'])
        merged_df = merged_df.drop(columns=['movieNm_box', 'movieNm_detail'])

    if 'openDt_detail' in merged_df.columns:
        merged_df['openDt'] = merged_df['openDt_detail'].fillna(merged_df['openDt_box'])
        merged_df = merged_df.drop(columns=['openDt_box', 'openDt_detail'])

    # 최종 데이터 저장
    collector.save_data(merged_df, '../data/raw/kobis_merged.csv')

    logger.info("=" * 60)
    logger.info(f"✅ 데이터 수집 완료: 총 {len(merged_df)}편")
    logger.info("=" * 60)

    # 통계 출력
    print("\n[수집 데이터 통계]")
    print(f"총 영화 수: {len(merged_df)}편")
    print(f"총 누적 관객수: {merged_df['audiAcc'].sum():,}명")
    print(f"평균 관객수: {merged_df['audiAcc'].mean():,.0f}명")
    print(f"\n장르별 분포:")
    print(merged_df['genres'].value_counts().head(10))


if __name__ == "__main__":
    main()
