"""
누락된 영화들을 재수집하는 스크립트
다양한 HTML 패턴을 시도하여 평점 추출
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import random
from typing import Dict, Optional
from urllib.parse import quote
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FlexibleRatingCollector:
    """다양한 HTML 패턴을 지원하는 유연한 평점 수집기"""

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

    def get_rating_flexible(self, movie_name: str) -> Optional[Dict]:
        """
        여러 HTML 패턴을 시도하여 평점 수집
        """
        self.init_driver()

        search_query = f'영화 {movie_name} 관람평'
        encoded_query = quote(search_query)
        search_url = f"https://search.naver.com/search.naver?query={encoded_query}&where=nexearch"

        try:
            time.sleep(random.uniform(self.delay, self.delay + 1))
            self.driver.get(search_url)
            time.sleep(3)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # 결과 저장
            result = {
                'movie_name': movie_name,
                'viewer_total': None,
                'viewer_male': None,
                'viewer_female': None,
                'netizen_total': None,
                'netizen_male': None,
                'netizen_female': None,
                'viewer_ratio_male': None,
                'viewer_ratio_female': None,
                'netizen_ratio_male': None,
                'netizen_ratio_female': None,
                'critic_rating_avg': None,
                'critic_rating_count': 0,
                'extraction_method': []  # 어떤 방법으로 추출했는지 기록
            }

            # 1. 평점 추출 - 여러 방법 시도
            ratings = self._extract_ratings_multi_method(soup)
            if ratings:
                result.update(ratings)

            # 2. 성별 비율 추출 - 여러 방법 시도
            ratios = self._extract_ratios_multi_method(soup)
            if ratios:
                result.update(ratios)

            # 3. 평론가 평점 추출 - 여러 방법 시도
            critic = self._extract_critic_multi_method(soup)
            if critic:
                result.update(critic)

            # 추출 성공 여부 확인
            success = any([
                result['viewer_total'],
                result['netizen_total'],
                result['critic_rating_avg']
            ])

            if success:
                logger.info(f"✅ '{movie_name}' - 방법: {', '.join(result['extraction_method'])}")
            else:
                logger.warning(f"❌ '{movie_name}' - 모든 방법 실패")

            return result

        except Exception as e:
            logger.error(f"'{movie_name}' 수집 실패: {e}")
            return None

    def _extract_ratings_multi_method(self, soup: BeautifulSoup) -> Optional[Dict]:
        """평점 추출 - 여러 방법 시도"""

        # 방법 1: area_star_number (기본)
        try:
            star_numbers = soup.find_all('span', class_='area_star_number')
            if len(star_numbers) >= 6:
                ratings = [s.get_text(strip=True) for s in star_numbers]
                return {
                    'viewer_total': ratings[0],
                    'viewer_male': ratings[1],
                    'viewer_female': ratings[2],
                    'netizen_total': ratings[3],
                    'netizen_male': ratings[4],
                    'netizen_female': ratings[5],
                    'extraction_method': ['area_star_number']
                }
        except:
            pass

        # 방법 2: class에 'star' 또는 'score' 포함
        try:
            star_elements = soup.find_all(class_=re.compile(r'star|score|rating', re.I))
            ratings = []
            for elem in star_elements:
                text = elem.get_text(strip=True)
                # 숫자.숫자 형태 찾기
                match = re.search(r'(\d+\.?\d*)', text)
                if match and 0 <= float(match.group(1)) <= 10:
                    ratings.append(match.group(1))

            if len(ratings) >= 6:
                return {
                    'viewer_total': ratings[0],
                    'viewer_male': ratings[1],
                    'viewer_female': ratings[2],
                    'netizen_total': ratings[3],
                    'netizen_male': ratings[4],
                    'netizen_female': ratings[5],
                    'extraction_method': ['star_score_pattern']
                }
        except:
            pass

        # 방법 3: strong 태그 내 숫자
        try:
            strong_numbers = soup.find_all('strong')
            ratings = []
            for strong in strong_numbers:
                text = strong.get_text(strip=True)
                match = re.search(r'(\d+\.?\d*)', text)
                if match and 0 <= float(match.group(1)) <= 10:
                    ratings.append(match.group(1))

            if len(ratings) >= 4:  # 최소 4개 (실관람객/네티즌 총점)
                return {
                    'viewer_total': ratings[0] if len(ratings) >= 1 else None,
                    'viewer_male': ratings[1] if len(ratings) >= 2 else None,
                    'viewer_female': ratings[2] if len(ratings) >= 3 else None,
                    'netizen_total': ratings[3] if len(ratings) >= 4 else None,
                    'netizen_male': ratings[4] if len(ratings) >= 5 else None,
                    'netizen_female': ratings[5] if len(ratings) >= 6 else None,
                    'extraction_method': ['strong_numbers']
                }
        except:
            pass

        return None

    def _extract_ratios_multi_method(self, soup: BeautifulSoup) -> Optional[Dict]:
        """성별 비율 추출 - 여러 방법 시도"""

        # 방법 1: area_category > em.num (기본)
        try:
            category_nums = []
            area_categories = soup.find_all('ul', class_='area_category')

            for category in area_categories:
                nums = category.find_all('em', class_='num')
                for num in nums:
                    num_text = num.get_text(strip=True)
                    category_nums.append(num_text)

            if len(category_nums) >= 4:
                return {
                    'viewer_ratio_male': category_nums[0],
                    'viewer_ratio_female': category_nums[1],
                    'netizen_ratio_male': category_nums[2],
                    'netizen_ratio_female': category_nums[3],
                    'extraction_method': ['area_category_num']
                }
        except:
            pass

        # 방법 2: em 태그 + % 기호
        try:
            em_elements = soup.find_all('em')
            ratios = []
            for em in em_elements:
                text = em.get_text(strip=True)
                # 숫자% 또는 숫자 형태
                match = re.search(r'(\d+)%?', text)
                if match and 0 <= int(match.group(1)) <= 100:
                    ratios.append(match.group(1))

            if len(ratios) >= 4:
                return {
                    'viewer_ratio_male': ratios[0],
                    'viewer_ratio_female': ratios[1],
                    'netizen_ratio_male': ratios[2],
                    'netizen_ratio_female': ratios[3],
                    'extraction_method': ['em_percent_pattern']
                }
        except:
            pass

        return None

    def _extract_critic_multi_method(self, soup: BeautifulSoup) -> Optional[Dict]:
        """평론가 평점 추출 - 여러 방법 시도"""
        critic_ratings = []

        # 방법 1: lego_critic_outer (기본)
        try:
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

                    if critic_ratings:
                        numeric_ratings = [float(r) for r in critic_ratings]
                        avg = sum(numeric_ratings) / len(numeric_ratings)
                        return {
                            'critic_rating_avg': f"{avg:.2f}",
                            'critic_rating_count': len(critic_ratings),
                            'extraction_method': ['lego_critic_outer']
                        }
        except:
            pass

        # 방법 2: lego_movie_pure_star 직접 찾기
        try:
            pure_stars = soup.find_all('div', class_='lego_movie_pure_star')
            for pure_star in pure_stars:
                # 모든 텍스트에서 숫자 찾기
                text = pure_star.get_text(strip=True)
                cleaned_text = re.sub(r'별점\(10점\s*만점\s*중\)', '', text)
                numbers = re.findall(r'\d+(?:\.\d+)?', cleaned_text)

                # 0-10 범위 숫자만 선택
                for num in numbers:
                    if 0 <= float(num) <= 10:
                        critic_ratings.append(num)
                        break  # 첫 번째 유효한 숫자만

            if critic_ratings:
                numeric_ratings = [float(r) for r in critic_ratings]
                avg = sum(numeric_ratings) / len(numeric_ratings)
                return {
                    'critic_rating_avg': f"{avg:.2f}",
                    'critic_rating_count': len(critic_ratings),
                    'extraction_method': ['pure_star_direct']
                }
        except:
            pass

        # 방법 3: "평론가" 키워드 근처에서 찾기
        try:
            # 평론가 텍스트가 있는 영역 찾기
            elements = soup.find_all(text=re.compile(r'평론가', re.I))
            for elem in elements:
                parent = elem.parent
                # 부모 영역에서 숫자 찾기
                for _ in range(3):  # 최대 3단계 상위까지
                    if parent:
                        text = parent.get_text()
                        numbers = re.findall(r'\d+\.?\d*', text)
                        for num in numbers:
                            try:
                                if 0 <= float(num) <= 10:
                                    critic_ratings.append(num)
                            except:
                                pass
                        parent = parent.parent

            if critic_ratings:
                # 중복 제거
                critic_ratings = list(set(critic_ratings))[:10]  # 최대 10개
                numeric_ratings = [float(r) for r in critic_ratings]
                avg = sum(numeric_ratings) / len(numeric_ratings)
                return {
                    'critic_rating_avg': f"{avg:.2f}",
                    'critic_rating_count': len(critic_ratings),
                    'extraction_method': ['keyword_search']
                }
        except:
            pass

        return None


def retry_missing_movies():
    """누락된 영화들을 재수집"""

    # 누락 영화 목록 로드
    missing_file = '../data/raw/missing_movies_report.csv'
    try:
        missing_df = pd.read_csv(missing_file, encoding='utf-8-sig')
        movie_list = missing_df['movie_name'].tolist()
        logger.info(f"누락 영화 {len(movie_list)}편 로드 완료")
    except FileNotFoundError:
        logger.error(f"누락 영화 목록을 찾을 수 없습니다: {missing_file}")
        logger.error("먼저 save_missing_data.py를 실행하세요.")
        return

    # 재수집 시작
    collector = FlexibleRatingCollector(delay=2.0, headless=True)
    results = []

    try:
        from tqdm import tqdm
        for movie_name in tqdm(movie_list, desc="재수집 중"):
            result = collector.get_rating_flexible(movie_name)
            if result:
                results.append(result)
    finally:
        collector.close_driver()

    # 결과 저장
    if results:
        df = pd.DataFrame(results)

        # extraction_method 컬럼 제거 (저장 전)
        if 'extraction_method' in df.columns:
            # 방법을 문자열로 변환
            df['extraction_method'] = df['extraction_method'].apply(lambda x: ', '.join(x) if x else '')

        output_file = '../data/raw/naver_ratings_retry.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')

        logger.info(f"\n{'='*60}")
        logger.info(f"✅ 재수집 완료: {output_file}")
        logger.info(f"총 {len(results)}개 영화 재수집")

        # 성공률 계산
        success_count = sum(1 for r in results if r['viewer_total'] or r['netizen_total'])
        logger.info(f"성공: {success_count}편 ({success_count/len(results)*100:.1f}%)")
        logger.info(f"{'='*60}")

        return df
    else:
        logger.warning("재수집된 평점이 없습니다.")
        return None


if __name__ == '__main__':
    retry_missing_movies()
