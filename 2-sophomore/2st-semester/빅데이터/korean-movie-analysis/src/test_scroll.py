"""
스크롤 기능 테스트
"""
from naver_collector_v2 import NaverReviewCollector

def test_scroll():
    collector = NaverReviewCollector(delay=2.0, headless=False)  # 브라우저 보이게

    test_movies = ['기생충', '베테랑']

    for movie in test_movies:
        print(f"\n{'='*60}")
        print(f"테스트: {movie}")
        print('='*60)

        result = collector.collect_movie_data(movie)

        print(f"상태: {result['status']}")
        print(f"평점: {result['ratings']}")
        print(f"리뷰 수: {len(result['reviews'])}개")

        if result['reviews']:
            print(f"\n첫 번째 리뷰:")
            print(f"  {result['reviews'][0]}")
            print(f"\n마지막 리뷰:")
            print(f"  {result['reviews'][-1]}")

    collector.close_driver()
    print("\n테스트 완료!")

if __name__ == '__main__':
    test_scroll()
