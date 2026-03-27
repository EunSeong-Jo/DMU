"""
네이버 평점 데이터에서 누락된 항목이 있는 영화 확인
"""
import pandas as pd
import sys
import io

# UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_missing_data(csv_file='../data/raw/naver_ratings.csv'):
    """누락된 데이터가 있는 영화 확인"""

    # CSV 로드
    df = pd.read_csv(csv_file, encoding='utf-8-sig')

    print(f"전체 영화 수: {len(df)}편\n")
    print("="*80)

    # 주요 컬럼들
    important_columns = [
        'viewer_total', 'viewer_male', 'viewer_female',
        'netizen_total', 'netizen_male', 'netizen_female',
        'viewer_ratio_male', 'viewer_ratio_female',
        'netizen_ratio_male', 'netizen_ratio_female',
        'critic_rating_avg'
    ]

    # 1. 완전히 누락된 영화 (모든 평점 데이터 없음)
    print("\n[1] 모든 평점 데이터가 누락된 영화:")
    print("-"*80)

    completely_missing = []
    partially_missing = []

    for idx, row in df.iterrows():
        missing_fields = []

        for col in important_columns:
            # NaN이거나 빈 문자열인 경우
            if pd.isna(row[col]) or row[col] == '' or row[col] == 'None':
                missing_fields.append(col)

        if missing_fields:
            # 모든 viewer 평점이 없으면 완전 누락
            if all(col in missing_fields for col in ['viewer_total', 'netizen_total']):
                completely_missing.append(row['movie_name'])
            else:
                partially_missing.append({
                    'movie_name': row['movie_name'],
                    'missing_fields': missing_fields
                })

    if completely_missing:
        for i, movie in enumerate(completely_missing, 1):
            print(f"{i:2d}. {movie}")
    else:
        print("없음")

    print(f"\n완전 누락: {len(completely_missing)}편")

    # 2. 부분 누락된 영화
    print("\n" + "="*80)
    print("\n[2] 일부 항목만 누락된 영화:")
    print("-"*80)

    if partially_missing:
        for i, movie in enumerate(partially_missing, 1):
            # 누락 카테고리 분류
            missing_cats = []
            if 'netizen_total' in movie['missing_fields']:
                missing_cats.append('네티즌평점')
            if 'viewer_ratio_male' in movie['missing_fields']:
                missing_cats.append('성별비율')
            if 'critic_rating_avg' in movie['missing_fields']:
                missing_cats.append('평론가평점')

            print(f"{i:2d}. {movie['movie_name']} - 누락: {', '.join(missing_cats)}")
    else:
        print("없음")

    print(f"\n부분 누락: {len(partially_missing)}편")

    missing_movies = completely_missing + [m['movie_name'] for m in partially_missing]

    # 3. 평론가 평점이 0인 영화
    print("\n" + "="*80)
    print("\n[3] 평론가 평점이 없는 영화 (critic_rating_count = 0):")
    print("-"*80)

    no_critic_movies = df[df['critic_rating_count'] == 0]['movie_name'].tolist()

    if no_critic_movies:
        # 5개씩 한 줄에 출력
        for i in range(0, len(no_critic_movies), 5):
            batch = no_critic_movies[i:i+5]
            print(", ".join(batch))
    else:
        print("없음")

    print(f"\n평론가 평점 없음: {len(no_critic_movies)}편")

    # 4. 데이터 완전성 통계
    print("\n" + "="*80)
    print("\n[4] 데이터 완전성 통계:")
    print("-"*80)

    complete_movies = len(df) - len(missing_movies)
    print(f"✅ 완전한 데이터:  {complete_movies:3d}편 ({complete_movies/len(df)*100:5.1f}%)")
    print(f"⚠️  완전 누락:     {len(completely_missing):3d}편 ({len(completely_missing)/len(df)*100:5.1f}%)")
    print(f"⚠️  부분 누락:     {len(partially_missing):3d}편 ({len(partially_missing)/len(df)*100:5.1f}%)")
    print(f"📊 평론가평점없음: {len(no_critic_movies):3d}편 ({len(no_critic_movies)/len(df)*100:5.1f}%)")

    print("\n" + "="*80)

    return {
        'total_movies': len(df),
        'missing_movies': len(missing_movies),
        'no_critic_movies': len(no_critic_movies),
        'missing_list': missing_movies,
        'no_critic_list': no_critic_movies
    }


if __name__ == '__main__':
    result = check_missing_data()
