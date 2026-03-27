"""
네이버 평점 데이터에서 누락된 항목을 파일로 저장
"""
import pandas as pd
import sys
import io

# UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def save_missing_data(csv_file='../data/raw/naver_ratings.csv',
                      output_file='../data/raw/missing_movies_report.txt'):
    """누락된 데이터를 파일로 저장"""

    # CSV 로드
    df = pd.read_csv(csv_file, encoding='utf-8-sig')

    # 주요 컬럼들
    important_columns = [
        'viewer_total', 'viewer_male', 'viewer_female',
        'netizen_total', 'netizen_male', 'netizen_female',
        'viewer_ratio_male', 'viewer_ratio_female',
        'netizen_ratio_male', 'netizen_ratio_female',
        'critic_rating_avg'
    ]

    # 결과를 저장할 리스트
    output_lines = []

    output_lines.append("="*80)
    output_lines.append("네이버 영화 평점 데이터 누락 항목 리포트")
    output_lines.append("="*80)
    output_lines.append(f"\n전체 영화 수: {len(df)}편\n")

    # 1. 완전히 누락된 영화 (모든 평점 데이터 없음)
    completely_missing = []
    partially_missing = []

    for idx, row in df.iterrows():
        missing_fields = []

        for col in important_columns:
            if pd.isna(row[col]) or row[col] == '' or row[col] == 'None':
                missing_fields.append(col)

        if missing_fields:
            # 모든 viewer 평점과 netizen 평점이 없으면 완전 누락
            if all(col in missing_fields for col in ['viewer_total', 'netizen_total']):
                completely_missing.append(row['movie_name'])
            else:
                partially_missing.append({
                    'movie_name': row['movie_name'],
                    'missing_fields': missing_fields
                })

    # 완전 누락 영화 저장
    output_lines.append("="*80)
    output_lines.append("[1] 모든 평점 데이터가 누락된 영화")
    output_lines.append("="*80)

    if completely_missing:
        for i, movie in enumerate(completely_missing, 1):
            output_lines.append(f"{i:2d}. {movie}")
    else:
        output_lines.append("없음")

    output_lines.append(f"\n완전 누락: {len(completely_missing)}편\n")

    # 부분 누락 영화 저장
    output_lines.append("="*80)
    output_lines.append("[2] 일부 항목만 누락된 영화")
    output_lines.append("="*80)

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

            output_lines.append(f"{i:2d}. {movie['movie_name']}")
            output_lines.append(f"    누락: {', '.join(missing_cats)}")
    else:
        output_lines.append("없음")

    output_lines.append(f"\n부분 누락: {len(partially_missing)}편\n")

    # 평론가 평점이 없는 영화
    output_lines.append("="*80)
    output_lines.append("[3] 평론가 평점이 없는 영화 (critic_rating_count = 0)")
    output_lines.append("="*80)

    no_critic_movies = df[df['critic_rating_count'] == 0]['movie_name'].tolist()

    if no_critic_movies:
        for i in range(0, len(no_critic_movies), 5):
            batch = no_critic_movies[i:i+5]
            output_lines.append(", ".join(batch))
    else:
        output_lines.append("없음")

    output_lines.append(f"\n평론가 평점 없음: {len(no_critic_movies)}편\n")

    # 통계 요약
    output_lines.append("="*80)
    output_lines.append("[4] 데이터 완전성 통계")
    output_lines.append("="*80)

    missing_count = len(completely_missing) + len(partially_missing)
    complete_movies = len(df) - missing_count

    output_lines.append(f"✅ 완전한 데이터:  {complete_movies:3d}편 ({complete_movies/len(df)*100:5.1f}%)")
    output_lines.append(f"⚠️  완전 누락:     {len(completely_missing):3d}편 ({len(completely_missing)/len(df)*100:5.1f}%)")
    output_lines.append(f"⚠️  부분 누락:     {len(partially_missing):3d}편 ({len(partially_missing)/len(df)*100:5.1f}%)")
    output_lines.append(f"📊 평론가평점없음: {len(no_critic_movies):3d}편 ({len(no_critic_movies)/len(df)*100:5.1f}%)")
    output_lines.append("="*80)

    # 파일 저장
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"✅ 누락 데이터 리포트 저장 완료: {output_file}")
    print(f"\n요약:")
    print(f"  - 전체 영화: {len(df)}편")
    print(f"  - 완전 누락: {len(completely_missing)}편")
    print(f"  - 부분 누락: {len(partially_missing)}편")
    print(f"  - 평론가평점없음: {len(no_critic_movies)}편")

    # CSV로도 저장
    csv_output = output_file.replace('.txt', '.csv')

    # 누락 영화 목록 생성
    missing_df_data = []

    for movie in completely_missing:
        missing_df_data.append({
            'movie_name': movie,
            'missing_type': '완전누락',
            'missing_details': '모든 평점 데이터 없음'
        })

    for movie in partially_missing:
        missing_cats = []
        if 'netizen_total' in movie['missing_fields']:
            missing_cats.append('네티즌평점')
        if 'viewer_ratio_male' in movie['missing_fields']:
            missing_cats.append('성별비율')
        if 'critic_rating_avg' in movie['missing_fields']:
            missing_cats.append('평론가평점')

        missing_df_data.append({
            'movie_name': movie['movie_name'],
            'missing_type': '부분누락',
            'missing_details': ', '.join(missing_cats)
        })

    if missing_df_data:
        missing_df = pd.DataFrame(missing_df_data)
        missing_df.to_csv(csv_output, index=False, encoding='utf-8-sig')
        print(f"✅ 누락 데이터 CSV 저장 완료: {csv_output}")

    return {
        'total': len(df),
        'complete': complete_movies,
        'completely_missing': len(completely_missing),
        'partially_missing': len(partially_missing),
        'no_critic': len(no_critic_movies)
    }


if __name__ == '__main__':
    result = save_missing_data()
    print(f"\n작업 완료!")
