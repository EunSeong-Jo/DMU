"""
KOBIS API를 사용하여 2014-2024년 모든 한국 영화 수집
"""

import os
import time
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

class AllMovieCollector:
    """KOBIS API로 모든 한국 영화 수집"""

    def __init__(self):
        self.api_key = os.getenv('KOBIS_API_KEY')
        self.base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest"
        self.session = requests.Session()
        self.delay = 1.0  # API 호출 간격 (초)

    def get_movie_list_by_date_range(self, start_year: str, end_year: str,
                                      page: int = 1, items_per_page: int = 100) -> Optional[Dict]:
        """
        연도 범위로 영화 목록 조회

        Args:
            start_year: 개봉 시작연도 (YYYY)
            end_year: 개봉 종료연도 (YYYY)
            page: 페이지 번호
            items_per_page: 페이지당 결과 수 (최대 100)
        """
        url = f"{self.base_url}/movie/searchMovieList.json"

        params = {
            'key': self.api_key,
            'openStartDt': start_year,
            'openEndDt': end_year,
            'curPage': page,
            'itemPerPage': items_per_page
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # 오류 응답 확인
            if 'faultInfo' in data:
                print(f"[ERROR] API 오류: {data['faultInfo'].get('message', 'Unknown error')}")
                return None

            return data
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] API 요청 실패 ({start_year}~{end_year}, page {page}): {e}")
            return None

    def get_movie_detail(self, movie_code: str) -> Optional[Dict]:
        """영화 상세 정보 조회"""
        url = f"{self.base_url}/movie/searchMovieInfo.json"

        params = {
            'key': self.api_key,
            'movieCd': movie_code
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get('movieInfoResult') and data['movieInfoResult'].get('movieInfo'):
                return data['movieInfoResult']['movieInfo']
            return None
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] 영화 상세 정보 요청 실패 (movieCd: {movie_code}): {e}")
            return None

    def collect_all_movies_by_year(self, year: int) -> List[Dict]:
        """특정 연도의 모든 한국 영화 수집"""
        year_str = str(year)

        all_movies = []
        page = 1

        print(f"\n[+] {year}년 영화 목록 수집 중...")

        while True:
            time.sleep(self.delay)

            result = self.get_movie_list_by_date_range(year_str, year_str, page, items_per_page=100)

            if not result or 'movieListResult' not in result:
                break

            movie_list = result['movieListResult'].get('movieList', [])

            if not movie_list:
                break

            all_movies.extend(movie_list)

            # 다음 페이지가 있는지 확인
            total_count = int(result['movieListResult'].get('totCnt', 0))
            current_count = page * 100

            if current_count >= total_count:
                break

            page += 1

        print(f"[OK] {year}년: {len(all_movies)}편 발견")
        return all_movies

    def enrich_movie_data(self, movie_list: List[Dict]) -> List[Dict]:
        """영화 목록에 상세 정보 추가"""
        enriched_movies = []

        print(f"\n[+] 상세 정보 수집 중... (총 {len(movie_list)}편)")

        for movie in tqdm(movie_list, desc="상세정보"):
            time.sleep(self.delay)

            movie_code = movie.get('movieCd')
            if not movie_code:
                continue

            detail = self.get_movie_detail(movie_code)

            if not detail:
                continue

            # 기본 정보 추출
            enriched = {
                'movieCd': movie_code,
                'movieNm': detail.get('movieNm', ''),
                'movieNmEn': detail.get('movieNmEn', ''),
                'openDt': detail.get('openDt', ''),
                'prdtYear': detail.get('prdtYear', ''),
                'showTm': detail.get('showTm', ''),
                'typeNm': detail.get('typeNm', ''),
                'prdtStatNm': detail.get('prdtStatNm', ''),
                'nationNm': detail.get('nations', [{}])[0].get('nationNm', '') if detail.get('nations') else '',
            }

            # 장르 추출
            genres = detail.get('genres', [])
            enriched['genres'] = ','.join([g.get('genreNm', '') for g in genres]) if genres else ''

            # 감독 추출
            directors = detail.get('directors', [])
            enriched['directors'] = ','.join([d.get('peopleNm', '') for d in directors]) if directors else ''

            # 배우 추출 (주연급 5명)
            actors = detail.get('actors', [])[:5]
            enriched['actors'] = ','.join([a.get('peopleNm', '') for a in actors]) if actors else ''

            # 관람등급 추출
            audits = detail.get('audits', [])
            enriched['watchGradeNm'] = audits[0].get('watchGradeNm', '') if audits else ''

            # 제작사 추출
            companies = detail.get('companys', [])
            prod_companies = [c.get('companyNm', '') for c in companies if c.get('companyPartNm') == '제작사']
            enriched['prod_company'] = ','.join(prod_companies) if prod_companies else ''

            # 한국 영화만 필터링 (nationNm에 '한국' 포함)
            if '한국' in enriched['nationNm']:
                enriched_movies.append(enriched)

        return enriched_movies

    def collect_all(self, start_year: int = 2024, end_year: int = 2024) -> pd.DataFrame:
        """전체 기간 모든 영화 수집"""
        print(f"\n{'='*60}")
        print(f"[START] KOBIS 한국 영화 수집 시작")
        print(f"[INFO] 기간: {start_year}년 ~ {end_year}년")
        print(f"[INFO] 한국 영화만 필터링 (nationNm='한국')")
        print(f"{'='*60}")

        all_movies = []

        # 연도별로 수집
        for year in range(start_year, end_year + 1):
            year_movies = self.collect_all_movies_by_year(year)
            all_movies.extend(year_movies)

        print(f"\n[INFO] 총 {len(all_movies)}편의 영화 발견")

        # 상세 정보 수집
        enriched_movies = self.enrich_movie_data(all_movies)

        # DataFrame 생성
        df = pd.DataFrame(enriched_movies)

        if len(df) > 0:
            # 개봉일 기준 정렬
            df['openDt'] = pd.to_datetime(df['openDt'], format='%Y%m%d', errors='coerce')
            df = df.sort_values('openDt').reset_index(drop=True)

        print(f"\n[OK] 최종 수집 완료: {len(df)}편")

        return df


def main():
    """메인 실행 함수"""

    # 수집기 초기화
    collector = AllMovieCollector()

    # 2024년 영화 수집 (최근 영화계 동향 분석)
    df = collector.collect_all(start_year=2024, end_year=2024)

    # 데이터 저장
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, 'korean_movies_2024.csv')
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"\n{'='*60}")
    print(f"[SAVE] 저장 완료: {output_file}")
    print(f"[INFO] 총 {len(df)}편의 영화 정보 저장")
    print(f"{'='*60}")

    # 기본 통계
    print("\n[STATS] 수집 통계:")
    print(f"- 연도별 분포:")
    df['year'] = df['openDt'].dt.year
    year_counts = df['year'].value_counts().sort_index()
    for year, count in year_counts.items():
        print(f"  {int(year)}년: {count}편")

    print(f"\n- 장르별 분포 (Top 10):")
    all_genres = df['genres'].str.split(',', expand=True).stack().value_counts()
    for genre, count in all_genres.head(10).items():
        print(f"  {genre}: {count}편")

    print(f"\n- 관람등급 분포:")
    grade_counts = df['watchGradeNm'].value_counts()
    for grade, count in grade_counts.items():
        print(f"  {grade}: {count}편")


if __name__ == "__main__":
    main()
