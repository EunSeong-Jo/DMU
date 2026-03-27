"""
연도 검증 기능이 있는 스마트 평점 수집기
검색 결과의 영화 연도를 확인하여 올바른 영화인지 검증
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import Dict, Optional
from tqdm import tqdm
import random
from urllib.parse import quote
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SmartRatingCollector:
    """연도 검증 기능이 있는 스마트 평점 수집기"""

    def __init__(self, delay: float = 2.0, headless: bool = True):
        self.delay = delay
        self.headless = headless
        self.driver = None

    def init_driver(self):
        """Selenium 드라이버 초기화"""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

            if self.headless:
                chrome_options.add_argument('--headless=new')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("드라이버 초기화 완료")

    def close_driver(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def extract_year_from_page(self, soup: BeautifulSoup, expected_year: int) -> Optional[int]:
        """
        검색 결과 페이지에서 영화 연도 추출
        div.sub_title > span.txt에서 연도 추출

        Args:
            soup: BeautifulSoup 객체
            expected_year: 기대하는 연도 (KOBIS 데이터)

        Returns:
            추출된 연도 또는 None
        """
        try:
            # div.sub_title > span.txt 모두 찾기
            sub_titles = soup.find_all('div', class_='sub_title')

            all_years = []

            for sub_title in sub_titles:
                txt_spans = sub_title.find_all('span', class_='txt')
                for txt_span in txt_spans:
                    text = txt_span.get_text(strip=True)
                    # 모든 4자리 숫자 찾기
                    year_matches = re.findall(r'\b(\d{4})\b', text)
                    for year_str in year_matches:
                        year = int(year_str)
                        # 1900-2030 사이의 합리적인 연도만
                        if 1900 <= year <= 2030:
                            all_years.append(year)
                            logger.debug(f"페이지에서 발견한 연도: {year} (텍스트: {text})")

            # 기대하는 연도가 발견된 연도 목록에 있는지 확인
            if expected_year in all_years:
                logger.debug(f"기대 연도 {expected_year} 발견!")
                return expected_year
            elif all_years:
                # 기대 연도가 없으면 가장 가까운 연도 반환
                closest_year = min(all_years, key=lambda y: abs(y - expected_year))
                logger.debug(f"⚠️  기대 연도 {expected_year} 없음, 가장 가까운 연도: {closest_year}")
                return closest_year
            else:
                logger.debug(f"❌ 페이지에서 연도를 찾을 수 없음")
                return None

        except Exception as e:
            logger.debug(f"연도 추출 실패: {e}")
            return None

    def get_rating_with_year_check(self, movie_name: str, expected_year: int) -> Optional[Dict]:
        """
        영화 평점 수집 (연도 검증 포함)

        Args:
            movie_name: 영화 제목
            expected_year: 예상 개봉년도 (KOBIS 데이터의 개봉년도)

        Returns:
            평점 딕셔너리 또는 None
        """
        self.init_driver()

        # 1차 시도: "영화 {제목} 관람평"
        search_query = f'영화 {movie_name} 관람평'
        result = self._try_search(movie_name, search_query, expected_year)

        if result is None:
            # 2차 시도: "{제목} 관람평" (영화 키워드 제거)
            logger.info(f"'{movie_name}' - 연도 불일치, 재시도 (영화 키워드 제거)")
            search_query = f'{movie_name} 관람평'
            result = self._try_search(movie_name, search_query, expected_year, is_retry=True)

        return result

    def _try_search(self, movie_name: str, search_query: str, expected_year: int, is_retry: bool = False) -> Optional[Dict]:
        """
        실제 검색 수행 및 데이터 추출

        Args:
            movie_name: 영화 제목
            search_query: 검색어
            expected_year: 예상 개봉년도
            is_retry: 재시도 여부
        """
        try:
            time.sleep(random.uniform(self.delay, self.delay + 1))

            # URL 생성 및 접근
            encoded_query = quote(search_query)
            search_url = f"https://search.naver.com/search.naver?query={encoded_query}&where=nexearch"

            logger.debug(f"검색 URL: {search_url}")

            self.driver.get(search_url)
            time.sleep(3)

            # HTML 파싱
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # 연도 확인 (expected_year를 전달)
            page_year = self.extract_year_from_page(soup, expected_year)

            if page_year:
                year_diff = abs(page_year - expected_year)

                # 연도가 1년 이상 차이나면 잘못된 영화
                if year_diff > 1:
                    logger.warning(f"'{movie_name}' - 연도 불일치 (예상: {expected_year}, 검색결과: {page_year})")
                    if not is_retry:
                        return None  # 재시도 필요
                    else:
                        logger.warning(f"'{movie_name}' - 재시도에도 연도 불일치, 데이터 수집 중단")
                        return None
                else:
                    logger.debug(f"'{movie_name}' - 연도 일치 확인 (예상: {expected_year}, 검색결과: {page_year})")
            else:
                logger.warning(f"'{movie_name}' - 페이지에서 연도를 찾을 수 없음")

            # 평점 데이터 추출
            result = self._extract_all_ratings(soup, movie_name)

            if result:
                result['search_query'] = search_query
                result['page_year'] = page_year
                result['expected_year'] = expected_year
                result['year_matched'] = (page_year == expected_year) if page_year else None

            return result

        except Exception as e:
            logger.error(f"'{movie_name}' 검색 실패: {e}")
            return None

    def _extract_all_ratings(self, soup: BeautifulSoup, movie_name: str) -> Optional[Dict]:
        """모든 평점 데이터 추출"""

        # 1. 실관람객/네티즌 평점
        star_numbers = soup.find_all('span', class_='area_star_number')
        all_star_ratings = [s.get_text(strip=True) for s in star_numbers]

        viewer_total = all_star_ratings[0] if len(all_star_ratings) >= 1 else None
        viewer_male = all_star_ratings[1] if len(all_star_ratings) >= 2 else None
        viewer_female = all_star_ratings[2] if len(all_star_ratings) >= 3 else None
        netizen_total = all_star_ratings[3] if len(all_star_ratings) >= 4 else None
        netizen_male = all_star_ratings[4] if len(all_star_ratings) >= 5 else None
        netizen_female = all_star_ratings[5] if len(all_star_ratings) >= 6 else None

        # 2. 성별 비율
        category_nums = []
        area_categories = soup.find_all('ul', class_='area_category')

        for category in area_categories:
            nums = category.find_all('em', class_='num')
            for num in nums:
                category_nums.append(num.get_text(strip=True))

        viewer_ratio_male = category_nums[0] if len(category_nums) >= 1 else None
        viewer_ratio_female = category_nums[1] if len(category_nums) >= 2 else None
        netizen_ratio_male = category_nums[2] if len(category_nums) >= 3 else None
        netizen_ratio_female = category_nums[3] if len(category_nums) >= 4 else None

        # 3. 평론가 평점
        critic_ratings = []
        critic_outer = soup.find('div', class_='lego_critic_outer')

        if critic_outer:
            area_ulist = critic_outer.find('ul', class_='area_ulist')
            if area_ulist:
                critic_items = area_ulist.find_all('li')

                for item in critic_items:
                    pure_star = item.find('div', class_='lego_movie_pure_star')
                    if pure_star:
                        text_box = pure_star.find('div', class_='area_text_box')
                        if text_box:
                            text_content = text_box.get_text(strip=True)
                            cleaned_text = re.sub(r'별점\(10점\s*만점\s*중\)', '', text_content)
                            numbers = re.findall(r'\d+(?:\.\d+)?', cleaned_text)
                            if numbers:
                                critic_ratings.append(numbers[0])

        critic_rating_avg = None
        if critic_ratings:
            try:
                numeric_ratings = [float(r) for r in critic_ratings]
                critic_rating_avg = sum(numeric_ratings) / len(numeric_ratings)
            except:
                pass

        # 결과 구성
        result = {
            'movie_name': movie_name,
            'viewer_total': viewer_total,
            'viewer_male': viewer_male,
            'viewer_female': viewer_female,
            'netizen_total': netizen_total,
            'netizen_male': netizen_male,
            'netizen_female': netizen_female,
            'viewer_ratio_male': viewer_ratio_male,
            'viewer_ratio_female': viewer_ratio_female,
            'netizen_ratio_male': netizen_ratio_male,
            'netizen_ratio_female': netizen_ratio_female,
            'critic_rating_avg': f"{critic_rating_avg:.2f}" if critic_rating_avg else None,
            'critic_rating_count': len(critic_ratings),
        }

        # 하나라도 데이터가 있으면 성공
        has_data = any([viewer_total, netizen_total, critic_rating_avg])

        if has_data:
            logger.info(f"'{movie_name}' - 수집 성공")
            return result
        else:
            logger.warning(f"❌ '{movie_name}' - 데이터 없음")
            return None

    def collect_with_kobis_data(self, kobis_file='../data/processed/korean_movies_with_star_power.csv',
                                 output_file='../data/raw/naver_ratings_220.csv',
                                 mismatch_file='../data/processed/year_mismatch_movies.csv',
                                 failed_file='../data/processed/failed_collection_movies.csv'):
        """
        KOBIS 데이터의 영화 목록과 개봉년도를 사용하여 수집

        Args:
            kobis_file: KOBIS 데이터 파일 경로 (220편 영화 데이터)
            output_file: 수집된 평점 저장 파일
            mismatch_file: 연도 불일치 영화 저장 파일
        """
        # KOBIS 데이터 로드
        try:
            kobis_df = pd.read_csv(kobis_file, encoding='utf-8-sig')
            logger.info(f"영화 데이터 로드: {len(kobis_df)}편")
        except FileNotFoundError:
            logger.error(f"영화 파일을 찾을 수 없습니다: {kobis_file}")
            return

        # 전체 220편 사용
        final_df = kobis_df.copy()

        logger.info(f"\n수집 대상: 총 {len(final_df)}편 (2014-2024)")

        # 수집 시작
        results = []
        year_mismatches = []  # 연도 불일치 영화 목록
        failed_movies = []  # 수집 실패 영화 목록

        try:
            for idx, row in tqdm(final_df.iterrows(), total=len(final_df), desc="평점 수집"):
                movie_name = row['movieNm']
                movie_cd = row['movieCd']

                # 개봉년도 추출 (year 컬럼 사용)
                expected_year = int(row['year'])

                # 평점 수집 (연도 검증 포함)
                result = self.get_rating_with_year_check(movie_name, expected_year)

                if result:
                    results.append(result)

                    # 연도 불일치 확인
                    if result.get('year_matched') == False:
                        year_mismatches.append({
                            'movieCd': movie_cd,
                            'movie_name': movie_name,
                            'expected_year': result['expected_year'],
                            'page_year': result['page_year'],
                            'year_diff': abs(result['page_year'] - result['expected_year']) if result['page_year'] else None,
                            'search_query': result['search_query'],
                            'has_data': bool(result['viewer_total'] or result['netizen_total'])
                        })
                else:
                    # 수집 실패한 영화 기록
                    failed_movies.append({
                        'movieCd': movie_cd,
                        'movie_name': movie_name,
                        'expected_year': expected_year,
                        'reason': '검색 결과 없음 또는 데이터 추출 실패'
                    })
                    logger.warning(f"❌ '{movie_name}' ({expected_year}) - 수집 실패")

        finally:
            self.close_driver()

        # 결과 CSV 저장
        if results:
            df = pd.DataFrame(results)

            import os
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"\n{'='*60}")
            logger.info(f"저장 완료: {output_file}")
            logger.info(f"총 {len(results)}개 영화 평점 수집")
            logger.info(f"{'='*60}")

        # 연도 불일치 영화 저장
        if year_mismatches:
            mismatch_df = pd.DataFrame(year_mismatches)

            import os
            os.makedirs(os.path.dirname(mismatch_file), exist_ok=True)

            mismatch_df.to_csv(mismatch_file, index=False, encoding='utf-8-sig')
            logger.info(f"\n{'='*60}")
            logger.info(f"⚠️  연도 불일치 영화 저장: {mismatch_file}")
            logger.info(f"총 {len(year_mismatches)}편")
            logger.info(f"{'='*60}")

            # 불일치 영화 출력
            print("\n연도 불일치 영화 목록:")
            print("-"*80)
            for i, item in enumerate(year_mismatches[:10], 1):  # 처음 10개만 출력
                print(f"{i:2d}. {item['movie_name']}")
                print(f"    KOBIS: {item['expected_year']}년 | 페이지: {item['page_year']}년 | 차이: {item['year_diff']}년")
                print(f"    검색어: {item['search_query']}")

            if len(year_mismatches) > 10:
                print(f"\n... 외 {len(year_mismatches) - 10}편 (전체 목록은 CSV 파일 참조)")

        # 수집 실패 영화 저장
        if failed_movies:
            failed_df = pd.DataFrame(failed_movies)

            import os
            os.makedirs(os.path.dirname(failed_file), exist_ok=True)

            failed_df.to_csv(failed_file, index=False, encoding='utf-8-sig')
            logger.info(f"\n{'='*60}")
            logger.info(f"❌ 수집 실패 영화 저장: {failed_file}")
            logger.info(f"총 {len(failed_movies)}편")
            logger.info(f"{'='*60}")

            # 실패 영화 출력
            print("\n수집 실패 영화 목록:")
            print("-"*80)
            for i, item in enumerate(failed_movies[:10], 1):  # 처음 10개만 출력
                print(f"{i:2d}. {item['movie_name']} ({item['expected_year']}년)")
                print(f"    사유: {item['reason']}")

            if len(failed_movies) > 10:
                print(f"\n... 외 {len(failed_movies) - 10}편 (전체 목록은 CSV 파일 참조)")

        if results:
            return df
        else:
            logger.warning("수집된 평점이 없습니다.")
            return None


def main():
    """메인 실행 함수"""
    collector = SmartRatingCollector(delay=2.0, headless=False)  # 브라우저 표시

    print("\n" + "="*80)
    print("🎬 네이버 평점 수집 시작 (220편)")
    print("="*80)

    df = collector.collect_with_kobis_data()

    if df is not None:
        print("\n" + "="*80)
        print("수집 완료!")
        print("="*80)
        print(f"총 수집: {len(df)}편")

        # 통계 출력
        print("\n=== 평점 데이터 통계 ===")
        print(f"실관람객 평점: {df['viewer_total'].notna().sum()}편")
        print(f"네티즌 평점: {df['netizen_total'].notna().sum()}편")
        print(f"평론가 평점: {df['critic_rating_avg'].notna().sum()}편")

        # 성공률 계산
        total_target = 220
        success_rate = (len(df) / total_target) * 100
        print(f"\n수집 성공률: {success_rate:.1f}% ({len(df)}/{total_target}편)")

        if len(df) < total_target:
            failed_count = total_target - len(df)
            print(f"수집 실패: {failed_count}편 (failed_collection_movies.csv 확인)")
    else:
        print("\n⚠️  수집된 데이터가 없습니다.")


if __name__ == '__main__':
    main()
