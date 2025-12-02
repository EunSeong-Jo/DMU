"""
데이터 수집 테스트 스크립트

소규모 데이터로 수집 코드를 테스트합니다.
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_kobis_api():
    """KOBIS API 연결 테스트"""
    logger.info("=" * 60)
    logger.info("KOBIS API 테스트 시작")
    logger.info("=" * 60)

    from kobis_collector import KOBISCollector

    # 환경변수 로드
    load_dotenv()
    api_key = os.getenv('KOBIS_API_KEY')

    if not api_key:
        logger.error("❌ KOBIS_API_KEY가 설정되지 않았습니다.")
        logger.error("   .env 파일에 API 키를 설정하세요.")
        return False

    collector = KOBISCollector(api_key=api_key, delay=0.5)

    # 1. 일별 박스오피스 조회 테스트
    test_date = "20241101"
    logger.info(f"1. 일별 박스오피스 조회 테스트 ({test_date})")

    result = collector.get_daily_boxoffice(test_date)

    if result and 'dailyBoxOfficeList' in result:
        logger.info(f"✅ 성공: {len(result['dailyBoxOfficeList'])}편의 영화 조회됨")
        for i, movie in enumerate(result['dailyBoxOfficeList'][:3], 1):
            logger.info(f"   {i}. {movie['movieNm']} (관객수: {int(movie['audiAcc']):,}명)")
    else:
        logger.error("❌ 실패: 박스오피스 데이터를 가져올 수 없습니다.")
        return False

    # 2. 영화 상세정보 조회 테스트
    if result and 'dailyBoxOfficeList' in result:
        test_movie_code = result['dailyBoxOfficeList'][0]['movieCd']
        test_movie_name = result['dailyBoxOfficeList'][0]['movieNm']

        logger.info(f"\n2. 영화 상세정보 조회 테스트 ({test_movie_name})")

        movie_info = collector.get_movie_info(test_movie_code)

        if movie_info:
            logger.info(f"✅ 성공: 영화 정보 조회됨")
            logger.info(f"   제목: {movie_info.get('movieNm')}")
            logger.info(f"   개봉일: {movie_info.get('openDt')}")
            logger.info(f"   장르: {[g['genreNm'] for g in movie_info.get('genres', [])]}")
            logger.info(f"   감독: {[d['peopleNm'] for d in movie_info.get('directors', [])]}")
        else:
            logger.error("❌ 실패: 영화 상세정보를 가져올 수 없습니다.")
            return False

    # 3. 소규모 데이터 수집 테스트 (최근 1주일)
    logger.info(f"\n3. 소규모 데이터 수집 테스트 (최근 1주일)")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    df = collector.collect_boxoffice_period(
        start_date=start_date,
        end_date=end_date,
        sample_interval=1
    )

    if len(df) > 0:
        logger.info(f"✅ 성공: {len(df)}편의 영화 수집됨")
        logger.info(f"\n   상위 5편:")
        for i, row in df.head(5).iterrows():
            logger.info(f"   {row['movieNm']}: {int(row['audiAcc']):,}명")

        # 테스트 데이터 저장
        os.makedirs('../data/test', exist_ok=True)
        test_file = '../data/test/kobis_test.csv'
        collector.save_data(df, test_file)
        logger.info(f"\n   테스트 데이터 저장: {test_file}")
    else:
        logger.error("❌ 실패: 데이터를 수집할 수 없습니다.")
        return False

    logger.info("\n" + "=" * 60)
    logger.info("✅ KOBIS API 테스트 통과!")
    logger.info("=" * 60)
    return True


def test_naver_crawler():
    """네이버 크롤러 테스트"""
    logger.info("\n" + "=" * 60)
    logger.info("네이버 크롤러 테스트 시작")
    logger.info("=" * 60)

    from naver_collector import NaverMovieCollector

    collector = NaverMovieCollector(delay=1.0, headless=False)

    # 테스트용 영화 목록
    test_movies = pd.DataFrame({
        'movieNm': ['베테랑2', '와일드 로봇', '트랜스포머 ONE'],
        'movieCd': ['test1', 'test2', 'test3']
    })

    logger.info(f"테스트 영화: {list(test_movies['movieNm'])}")

    try:
        # 1. 영화 검색 테스트
        logger.info("\n1. 영화 검색 테스트")
        test_movie = test_movies.iloc[0]['movieNm']

        movie_code = collector.search_movie(test_movie)

        if movie_code:
            logger.info(f"✅ 성공: '{test_movie}' 코드 = {movie_code}")
        else:
            logger.error(f"❌ 실패: '{test_movie}' 검색 실패")
            return False

        # 2. 평점 정보 테스트
        logger.info("\n2. 평점 정보 수집 테스트")

        rating_info = collector.get_movie_rating(movie_code)

        if rating_info['netizen_score']:
            logger.info(f"✅ 성공: 평점 정보 수집됨")
            logger.info(f"   네티즌 평점: {rating_info['netizen_score']}")
            logger.info(f"   평점 참여수: {rating_info['netizen_count']:,}명")
        else:
            logger.warning("⚠️  경고: 평점 정보를 찾을 수 없습니다.")

        # 3. 리뷰 수집 테스트 (5개만)
        logger.info("\n3. 리뷰 수집 테스트 (5개)")

        reviews = collector.get_movie_reviews(movie_code, max_reviews=5)

        if len(reviews) > 0:
            logger.info(f"✅ 성공: {len(reviews)}개 리뷰 수집됨")
            logger.info(f"\n   샘플 리뷰:")
            for i, review in enumerate(reviews[:2], 1):
                logger.info(f"   {i}. 평점 {review['score']}: {review['review_text'][:50]}...")
        else:
            logger.warning("⚠️  경고: 리뷰를 수집할 수 없습니다.")

        # 테스트 데이터 저장
        if len(reviews) > 0:
            os.makedirs('../data/test', exist_ok=True)
            reviews_df = pd.DataFrame(reviews)
            test_file = '../data/test/naver_test.csv'
            collector.save_data(reviews_df, test_file)
            logger.info(f"\n   테스트 데이터 저장: {test_file}")

        logger.info("\n" + "=" * 60)
        logger.info("✅ 네이버 크롤러 테스트 통과!")
        logger.info("=" * 60)
        return True

    except Exception as e:
        logger.error(f"❌ 테스트 실패: {e}")
        return False

    finally:
        collector.close_driver()


def validate_collected_data():
    """수집된 데이터 검증"""
    logger.info("\n" + "=" * 60)
    logger.info("수집 데이터 검증")
    logger.info("=" * 60)

    data_files = {
        'KOBIS 박스오피스': '../data/raw/kobis_boxoffice.csv',
        'KOBIS 상세정보': '../data/raw/kobis_movie_details.csv',
        'KOBIS 통합': '../data/raw/kobis_merged.csv',
        '네이버 평점': '../data/raw/naver_ratings.csv',
        '네이버 리뷰': '../data/raw/naver_reviews.csv'
    }

    all_valid = True

    for name, filepath in data_files.items():
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            logger.info(f"\n✅ {name}: {len(df):,}건")

            # 기본 통계
            if name == 'KOBIS 통합':
                logger.info(f"   평균 관객수: {df['audiAcc'].mean():,.0f}명")
                logger.info(f"   총 관객수: {df['audiAcc'].sum():,.0f}명")
                logger.info(f"   장르 분포:\n{df['genres'].value_counts().head(3)}")

            elif name == '네이버 평점':
                logger.info(f"   평균 네티즌 평점: {df['netizen_score'].mean():.2f}")
                logger.info(f"   평점 데이터 있음: {df['netizen_score'].notna().sum()}편")

            elif name == '네이버 리뷰':
                logger.info(f"   평균 리뷰 평점: {df['score'].mean():.2f}")
                logger.info(f"   평점별 분포:\n{df['score'].value_counts().sort_index()}")

        else:
            logger.warning(f"⚠️  {name}: 파일 없음 ({filepath})")
            all_valid = False

    logger.info("\n" + "=" * 60)
    if all_valid:
        logger.info("✅ 모든 데이터 파일 확인 완료!")
    else:
        logger.warning("⚠️  일부 데이터 파일이 없습니다.")
    logger.info("=" * 60)

    return all_valid


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print("🧪 데이터 수집 테스트 스크립트")
    print("=" * 60)

    # 사용자 선택
    print("\n테스트 옵션:")
    print("1. KOBIS API 테스트")
    print("2. 네이버 크롤러 테스트")
    print("3. 수집 데이터 검증")
    print("4. 전체 테스트")

    choice = input("\n선택하세요 (1-4): ").strip()

    if choice == '1':
        test_kobis_api()
    elif choice == '2':
        test_naver_crawler()
    elif choice == '3':
        validate_collected_data()
    elif choice == '4':
        logger.info("전체 테스트 실행\n")
        kobis_ok = test_kobis_api()
        if kobis_ok:
            naver_ok = test_naver_crawler()
            if naver_ok:
                validate_collected_data()
    else:
        logger.error("잘못된 선택입니다.")


if __name__ == "__main__":
    main()
