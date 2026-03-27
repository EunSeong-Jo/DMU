"""
KOBIS 과거 데이터 수집 - 주간 박스오피스 방식
- 2004-2018년 주간 박스오피스 데이터 수집 (TOP 10)
- 스타파워 분석을 위한 감독/배우 필모그래피 구축
- 개봉월 정보 포함 (계절 분석 가능)
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import logging
import time
from typing import Dict, List, Optional
from tqdm import tqdm
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeeklyKOBISCollector:
    """주간 박스오피스 KOBIS 데이터 수집기"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest"
        self.session = requests.Session()
        self.delay = 1.0  # API 호출 간 딜레이 (초)

    def get_weekly_boxoffice(self, target_date: str) -> Optional[List[Dict]]:
        """
        주간 박스오피스 조회

        Args:
            target_date: YYYYMMDD 형식

        Returns:
            주간 박스오피스 영화 리스트 (상위 10편)
        """
        url = f"{self.base_url}/boxoffice/searchWeeklyBoxOfficeList.json"
        params = {
            'key': self.api_key,
            'targetDt': target_date,
            'weekGb': '0'  # 0: 주간, 1: 주말, 2: 주중
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'boxOfficeResult' in data and 'weeklyBoxOfficeList' in data['boxOfficeResult']:
                return data['boxOfficeResult']['weeklyBoxOfficeList']
            else:
                return None

        except Exception as e:
            logger.error(f"주간 박스오피스 조회 실패 ({target_date}): {e}")
            return None

    def get_movie_details(self, movie_code: str) -> Optional[Dict]:
        """
        영화 상세정보 조회

        Args:
            movie_code: 영화 코드

        Returns:
            영화 상세정보
        """
        url = f"{self.base_url}/movie/searchMovieInfo.json"
        params = {
            'key': self.api_key,
            'movieCd': movie_code
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'movieInfoResult' in data:
                return data['movieInfoResult']['movieInfo']
            else:
                return None

        except Exception as e:
            logger.error(f"영화 상세정보 조회 실패 ({movie_code}): {e}")
            return None

    def get_week_dates(self, year: int) -> List[str]:
        """
        연도별 주차 날짜 생성 (매주 월요일 기준)

        Args:
            year: 연도

        Returns:
            주차별 날짜 리스트 (YYYYMMDD 형식)
        """
        dates = []
        current_date = datetime(year, 1, 1)

        # 첫 주 월요일 찾기
        days_to_monday = (7 - current_date.weekday()) % 7
        if days_to_monday > 0:
            current_date += timedelta(days=days_to_monday)

        # 해당 연도의 모든 월요일
        while current_date.year == year:
            dates.append(current_date.strftime('%Y%m%d'))
            current_date += timedelta(days=7)

        return dates

    def collect_year_range(self, start_year: int, end_year: int,
                           output_dir: Path) -> pd.DataFrame:
        """
        연도 범위 데이터 수집

        Args:
            start_year: 시작 연도
            end_year: 종료 연도
            output_dir: 출력 디렉토리

        Returns:
            수집된 데이터프레임
        """
        all_movies = []
        movie_codes_seen = set()

        total_years = end_year - start_year + 1
        logger.info(f"📅 {start_year}년 ~ {end_year}년 데이터 수집 시작")
        logger.info(f"예상 API 호출: 약 {total_years * 52}회")
        logger.info(f"예상 수집 기간: 약 {total_years * 52 / 60:.0f}분")

        # 연도별 수집
        for year in range(start_year, end_year + 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"📆 {year}년 주간 박스오피스 수집 중...")
            logger.info(f"{'='*60}")

            # 주차별 날짜 생성
            week_dates = self.get_week_dates(year)
            logger.info(f"주차 수: {len(week_dates)}주")

            # 주간 박스오피스 수집
            for week_date in tqdm(week_dates, desc=f"{year}년"):
                weekly_boxoffice = self.get_weekly_boxoffice(week_date)

                if weekly_boxoffice:
                    for movie in weekly_boxoffice:
                        movie_code = movie.get('movieCd')

                        # 중복 제거
                        if movie_code and movie_code not in movie_codes_seen:
                            movie_codes_seen.add(movie_code)

                            # 기본 정보 저장
                            movie_info = {
                                'movieCd': movie_code,
                                'movieNm': movie.get('movieNm'),
                                'openDt': movie.get('openDt'),
                                'audiAcc': movie.get('audiAcc'),
                                'salesAcc': movie.get('salesAcc'),
                                'rank': movie.get('rank'),
                                'rankOldAndNew': movie.get('rankOldAndNew')
                            }
                            all_movies.append(movie_info)

                # API 호출 제한 준수
                time.sleep(self.delay)

            logger.info(f"✅ {year}년 완료: 중복 제거 후 {len([m for m in all_movies if m.get('openDt', '')[:4] == str(year)])}편 추가")

            # 연도별 중간 저장
            if all_movies:
                temp_df = pd.DataFrame(all_movies)
                temp_file = output_dir / f'kobis_boxoffice_{year}.csv'
                temp_df.to_csv(temp_file, index=False, encoding='utf-8-sig')

        # 전체 데이터프레임 생성
        df = pd.DataFrame(all_movies)
        logger.info(f"\n🎉 1단계 완료: {len(df)}편 수집 (중복 제거 후)")

        return df

    def collect_movie_details_batch(self, df: pd.DataFrame,
                                    output_dir: Path) -> pd.DataFrame:
        """
        영화 상세정보 일괄 수집

        Args:
            df: 박스오피스 데이터프레임
            output_dir: 출력 디렉토리

        Returns:
            상세정보가 추가된 데이터프레임
        """
        logger.info(f"\n📋 2단계: 영화 상세정보 수집 시작")
        logger.info(f"대상: {len(df)}편")
        logger.info(f"예상 소요 시간: 약 {len(df) * 1.5 / 60:.0f}분")

        details_list = []

        for idx, row in tqdm(df.iterrows(), total=len(df), desc="상세정보 수집"):
            movie_code = row['movieCd']
            details = self.get_movie_details(movie_code)

            if details:
                detail_info = {
                    'movieCd': movie_code,
                    'genres': ','.join([g['genreNm'] for g in details.get('genres', [])]),
                    'directors': ','.join([d['peopleNm'] for d in details.get('directors', [])]),
                    'actors': ','.join([a['peopleNm'] for a in details.get('actors', [])[:5]]),  # 상위 5명
                    'showTm': details.get('showTm'),
                    'watchGradeNm': details.get('audits', [{}])[0].get('watchGradeNm') if details.get('audits') else None,
                    'nations': ','.join([n['nationNm'] for n in details.get('nations', [])])
                }
                details_list.append(detail_info)

                # 100편마다 중간 저장
                if len(details_list) % 100 == 0:
                    temp_df = pd.DataFrame(details_list)
                    temp_file = output_dir / 'kobis_details_temp.csv'
                    temp_df.to_csv(temp_file, index=False, encoding='utf-8-sig')
                    logger.info(f"💾 중간 저장: {len(details_list)}편")

            time.sleep(self.delay)

        # 상세정보 데이터프레임 생성
        if details_list:
            details_df = pd.DataFrame(details_list)
            logger.info(f"✅ 2단계 완료: {len(details_df)}편 상세정보 수집")

            # 병합
            merged_df = pd.merge(df, details_df, on='movieCd', how='left')
        else:
            logger.warning("⚠️ 수집된 상세정보가 없습니다!")
            # 빈 컬럼 추가
            merged_df = df.copy()
            merged_df['genres'] = None
            merged_df['directors'] = None
            merged_df['actors'] = None
            merged_df['showTm'] = None
            merged_df['watchGradeNm'] = None
            merged_df['nations'] = None

        return merged_df


def main():
    """메인 실행 함수"""

    # API 키 확인
    api_key = os.getenv('KOBIS_API_KEY')
    if not api_key:
        logger.error("❌ KOBIS_API_KEY가 설정되지 않았습니다.")
        logger.error("   .env 파일에 KOBIS_API_KEY를 설정하세요.")
        return

    # 출력 디렉토리 설정
    base_path = Path(__file__).parent.parent
    output_dir = base_path / 'data' / 'historical'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 수집기 초기화
    collector = WeeklyKOBISCollector(api_key)

    logger.info("="*60)
    logger.info("🎬 KOBIS 데이터 수집 (주간 박스오피스)")
    logger.info("="*60)
    logger.info(f"수집 범위: 2004년 ~ 2024년 (21년)")
    logger.info(f"수집 방식: 주간 박스오피스 TOP 10")
    logger.info(f"예상 영화 수: 약 1,500~2,000편 (중복 제거 후)")
    logger.info(f"예상 소요 시간:")
    logger.info(f"  - 1단계 (박스오피스): 18분 (1,092회 호출)")
    logger.info(f"  - 2단계 (상세정보): 25-35분")
    logger.info(f"  - 총: 약 45-55분")
    logger.info("="*60)

    # 사용자 확인
    print("\n⚠️  주의사항:")
    print("  - 전체 수집에 약 30-40분 소요됩니다")
    print("  - 주간 박스오피스 TOP 10만 수집합니다")
    print("  - 중간 저장이 자동으로 진행됩니다")
    print("  - openDt(개봉일) 정보가 포함되어 월별/계절별 분석 가능")
    print()

    proceed = input("계속 진행하시겠습니까? (y/n): ").strip().lower()
    if proceed != 'y':
        logger.info("수집을 중단합니다.")
        return

    try:
        # 1단계: 주간 박스오피스 수집
        logger.info("\n" + "="*60)
        logger.info("1단계: 주간 박스오피스 수집")
        logger.info("="*60)

        boxoffice_df = collector.collect_year_range(
            start_year=2004,
            end_year=2024,
            output_dir=output_dir
        )

        # 박스오피스 저장
        boxoffice_file = output_dir / 'kobis_boxoffice_2004_2024.csv'
        boxoffice_df.to_csv(boxoffice_file, index=False, encoding='utf-8-sig')
        logger.info(f"\n💾 1단계 결과 저장: {boxoffice_file}")
        logger.info(f"   총 {len(boxoffice_df)}편")

        # 2단계: 상세정보 수집
        logger.info("\n" + "="*60)
        logger.info("2단계: 영화 상세정보 수집")
        logger.info("="*60)

        merged_df = collector.collect_movie_details_batch(
            df=boxoffice_df,
            output_dir=output_dir
        )

        # 최종 저장
        final_file = output_dir / 'kobis_complete_2004_2024.csv'
        merged_df.to_csv(final_file, index=False, encoding='utf-8-sig')

        logger.info("\n" + "="*60)
        logger.info("🎉 전체 수집 완료!")
        logger.info("="*60)
        logger.info(f"📁 최종 파일: {final_file}")
        logger.info(f"📊 총 영화 수: {len(merged_df)}편")
        logger.info(f"📅 기간: 2004-2018 (15년)")
        logger.info(f"👥 감독 정보: {merged_df['directors'].notna().sum()}편")
        logger.info(f"🎭 배우 정보: {merged_df['actors'].notna().sum()}편")
        logger.info(f"🎬 장르 정보: {merged_df['genres'].notna().sum()}편")
        logger.info(f"📆 개봉일 정보: {merged_df['openDt'].notna().sum()}편")
        logger.info("="*60)

        # 연도별 통계
        # openDt 필드 정제: 빈 문자열/공백을 NaN으로 처리
        merged_df['openDt'] = merged_df['openDt'].replace(r'^\s*$', None, regex=True)

        # 유효한 날짜만 변환
        valid_dates = merged_df['openDt'].notna()
        if valid_dates.sum() > 0:
            merged_df.loc[valid_dates, 'year'] = pd.to_datetime(
                merged_df.loc[valid_dates, 'openDt'],
                errors='coerce'
            ).dt.year

            yearly_counts = merged_df['year'].value_counts().sort_index()
            logger.info("\n📊 연도별 영화 수:")
            for year, count in yearly_counts.items():
                if pd.notna(year):
                    logger.info(f"  {int(year)}년: {count}편")
        else:
            logger.warning("⚠️ 유효한 개봉일 정보가 없습니다.")

        logger.info("\n✅ 이제 스타파워 분석이 가능합니다!")
        logger.info("   - 2004-2018: 과거 필모그래피")
        logger.info("   - 2019-2024: 분석 대상 (236편)")
        logger.info("   - 개봉월 정보로 계절 분석 가능")

    except KeyboardInterrupt:
        logger.warning("\n⚠️  사용자에 의해 중단되었습니다.")
        logger.info("중간 저장 파일을 확인하세요:")
        logger.info(f"  {output_dir}")

    except Exception as e:
        logger.error(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
