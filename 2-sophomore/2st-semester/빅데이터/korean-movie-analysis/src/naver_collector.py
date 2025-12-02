"""
네이버 영화 데이터 크롤링 모듈

주요 기능:
1. 영화 제목으로 네이버 영화 코드 검색
2. 영화 평점 정보 수집
3. 관객 리뷰 수집
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re
import logging
from typing import List, Dict, Optional
from tqdm import tqdm
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NaverMovieCollector:
    """네이버 영화 데이터 수집 클래스"""

    BASE_URL = "https://movie.naver.com"
    SEARCH_URL = "https://movie.naver.com/movie/search/result.naver"

    def __init__(self, delay: float = 2.0, headless: bool = True):
        """
        Args:
            delay: 요청 간 대기 시간 (초)
            headless: 브라우저 백그라운드 실행 여부
        """
        self.delay = delay
        self.headless = headless
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def init_driver(self):
        """Selenium 웹드라이버 초기화"""
        if self.driver is None:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Selenium 드라이버 초기화 완료")

    def close_driver(self):
        """웹드라이버 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Selenium 드라이버 종료")

    def search_movie(self, movie_name: str) -> Optional[str]:
        """
        영화 제목으로 네이버 영화 코드 검색

        Args:
            movie_name: 영화 제목

        Returns:
            영화 코드 또는 None
        """
        params = {
            'query': movie_name,
            'section': 'movie',
            'ie': 'utf8'
        }

        try:
            response = self.session.get(self.SEARCH_URL, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 검색 결과에서 첫 번째 영화 선택
            movie_link = soup.select_one('ul.search_list_1 li:first-child a')

            if movie_link and 'href' in movie_link.attrs:
                href = movie_link['href']
                # code= 파라미터 추출
                match = re.search(r'code=(\d+)', href)
                if match:
                    movie_code = match.group(1)
                    logger.debug(f"영화 '{movie_name}' 코드: {movie_code}")
                    time.sleep(self.delay)
                    return movie_code

            logger.warning(f"영화 '{movie_name}' 검색 결과 없음")
            return None

        except Exception as e:
            logger.error(f"영화 검색 실패 ({movie_name}): {e}")
            return None

    def get_movie_rating(self, movie_code: str) -> Dict:
        """
        영화 평점 정보 수집

        Args:
            movie_code: 네이버 영화 코드

        Returns:
            평점 정보 딕셔너리
        """
        url = f"{self.BASE_URL}/movie/bi/mi/basic.naver?code={movie_code}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 네티즌 평점
            netizen_score_elem = soup.select_one('.score.score_left .star_score em')
            netizen_score = float(netizen_score_elem.text) if netizen_score_elem else None

            # 평점 참여 수
            netizen_count_elem = soup.select_one('.score.score_left .star_score + em + em')
            netizen_count = None
            if netizen_count_elem:
                count_text = netizen_count_elem.text.strip()
                match = re.search(r'([\d,]+)', count_text)
                if match:
                    netizen_count = int(match.group(1).replace(',', ''))

            # 기자/평론가 평점
            critic_score_elem = soup.select_one('.score.score_right .star_score em')
            critic_score = float(critic_score_elem.text) if critic_score_elem else None

            # 관람객 수
            audience_elem = soup.select_one('.special_lst .count')
            audience = None
            if audience_elem:
                aud_text = audience_elem.text.strip()
                match = re.search(r'([\d,]+)', aud_text)
                if match:
                    audience = int(match.group(1).replace(',', ''))

            time.sleep(self.delay)

            return {
                'naver_code': movie_code,
                'netizen_score': netizen_score,
                'netizen_count': netizen_count,
                'critic_score': critic_score,
                'audience_count': audience
            }

        except Exception as e:
            logger.error(f"평점 수집 실패 (코드: {movie_code}): {e}")
            return {
                'naver_code': movie_code,
                'netizen_score': None,
                'netizen_count': None,
                'critic_score': None,
                'audience_count': None
            }

    def get_movie_reviews(self, movie_code: str, max_reviews: int = 50) -> List[Dict]:
        """
        영화 리뷰 수집 (Selenium 사용)

        Args:
            movie_code: 네이버 영화 코드
            max_reviews: 최대 수집 리뷰 수

        Returns:
            리뷰 리스트
        """
        self.init_driver()

        url = f"{self.BASE_URL}/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false"

        reviews = []

        try:
            self.driver.get(url)
            time.sleep(2)

            page = 1
            max_pages = (max_reviews // 10) + 1

            while len(reviews) < max_reviews and page <= max_pages:
                # 리뷰 요소 찾기
                review_elements = self.driver.find_elements(By.CSS_SELECTOR, '.score_result ul li')

                for elem in review_elements:
                    if len(reviews) >= max_reviews:
                        break

                    try:
                        # 리뷰 텍스트
                        review_text_elem = elem.find_element(By.CSS_SELECTOR, '.score_reple p')
                        review_text = review_text_elem.text.strip()

                        # 평점
                        score_elem = elem.find_element(By.CSS_SELECTOR, '.star_score em')
                        score = int(score_elem.text)

                        # 작성일
                        date_elem = elem.find_element(By.CSS_SELECTOR, '.score_reple dt em:nth-of-type(2)')
                        date = date_elem.text.strip()

                        # 공감 수
                        sympathy_elem = elem.find_element(By.CSS_SELECTOR, '.btn_area .sympathy_count em')
                        sympathy = int(sympathy_elem.text)

                        reviews.append({
                            'naver_code': movie_code,
                            'review_text': review_text,
                            'score': score,
                            'date': date,
                            'sympathy': sympathy
                        })

                    except Exception as e:
                        logger.debug(f"리뷰 파싱 오류: {e}")
                        continue

                # 다음 페이지로 이동
                if len(reviews) < max_reviews and page < max_pages:
                    try:
                        next_btn = self.driver.find_element(By.CSS_SELECTOR, '.paging .pg_next')
                        next_btn.click()
                        time.sleep(random.uniform(1.5, 2.5))
                        page += 1
                    except:
                        logger.info(f"다음 페이지 없음 (페이지 {page})")
                        break

            logger.info(f"영화 코드 {movie_code}: {len(reviews)}개 리뷰 수집")

        except Exception as e:
            logger.error(f"리뷰 수집 실패 (코드: {movie_code}): {e}")

        return reviews

    def collect_movies_data(
        self,
        movie_list: pd.DataFrame,
        reviews_per_movie: int = 50
    ) -> tuple:
        """
        영화 목록에 대한 평점 및 리뷰 일괄 수집

        Args:
            movie_list: 영화 목록 데이터프레임 (movieNm 컬럼 필수)
            reviews_per_movie: 영화당 수집할 리뷰 수

        Returns:
            (평점 데이터프레임, 리뷰 데이터프레임)
        """
        logger.info(f"네이버 데이터 수집 시작: {len(movie_list)}편")

        ratings_data = []
        all_reviews = []

        for idx, row in tqdm(movie_list.iterrows(), total=len(movie_list), desc="네이버 데이터 수집"):
            movie_name = row['movieNm']

            # 1. 영화 코드 검색
            movie_code = self.search_movie(movie_name)

            if not movie_code:
                logger.warning(f"영화 '{movie_name}' 코드를 찾을 수 없음")
                continue

            # 2. 평점 정보 수집
            rating_info = self.get_movie_rating(movie_code)
            rating_info['movieNm'] = movie_name
            rating_info['movieCd'] = row.get('movieCd')
            ratings_data.append(rating_info)

            # 3. 리뷰 수집
            reviews = self.get_movie_reviews(movie_code, max_reviews=reviews_per_movie)
            for review in reviews:
                review['movieNm'] = movie_name
                review['movieCd'] = row.get('movieCd')
            all_reviews.extend(reviews)

            # 랜덤 대기 (크롤링 감지 방지)
            time.sleep(random.uniform(2, 4))

        logger.info(f"평점 수집: {len(ratings_data)}편")
        logger.info(f"리뷰 수집: {len(all_reviews)}개")

        ratings_df = pd.DataFrame(ratings_data)
        reviews_df = pd.DataFrame(all_reviews)

        return ratings_df, reviews_df

    def save_data(self, df: pd.DataFrame, filepath: str):
        """데이터프레임 저장"""
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        logger.info(f"데이터 저장 완료: {filepath}")


def main():
    """메인 실행 함수"""
    import os

    # KOBIS 데이터 로드
    kobis_file = '../data/raw/kobis_merged.csv'

    if not os.path.exists(kobis_file):
        logger.error(f"KOBIS 데이터 파일이 없습니다: {kobis_file}")
        logger.error("먼저 kobis_collector.py를 실행하세요.")
        return

    kobis_df = pd.read_csv(kobis_file)
    logger.info(f"KOBIS 데이터 로드: {len(kobis_df)}편")

    # 상위 100편만 테스트 (전체는 시간이 오래 걸림)
    # test_df = kobis_df.head(100)
    test_df = kobis_df  # 전체 수집

    # 수집기 초기화
    collector = NaverMovieCollector(delay=2.0, headless=False)  # headless=False로 브라우저 확인 가능

    try:
        # 데이터 수집
        ratings_df, reviews_df = collector.collect_movies_data(
            movie_list=test_df,
            reviews_per_movie=50
        )

        # 저장
        os.makedirs('../data/raw', exist_ok=True)
        collector.save_data(ratings_df, '../data/raw/naver_ratings.csv')
        collector.save_data(reviews_df, '../data/raw/naver_reviews.csv')

        logger.info("=" * 60)
        logger.info("✅ 네이버 데이터 수집 완료")
        logger.info("=" * 60)

        # 통계 출력
        print("\n[수집 데이터 통계]")
        print(f"평점 데이터: {len(ratings_df)}편")
        print(f"리뷰 데이터: {len(reviews_df)}개")
        print(f"\n평균 네티즌 평점: {ratings_df['netizen_score'].mean():.2f}")
        print(f"평균 리뷰 평점: {reviews_df['score'].mean():.2f}")

    finally:
        # 드라이버 종료
        collector.close_driver()


if __name__ == "__main__":
    main()
