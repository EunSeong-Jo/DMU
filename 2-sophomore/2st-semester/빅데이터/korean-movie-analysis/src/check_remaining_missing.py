"""
재수집 후에도 여전히 누락된 영화들을 확인
"""
import pandas as pd
import sys
import io

# UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def check_remaining_missing():
    """재수집 후 여전히 누락된 영화 확인"""

    # 1. 원본 데이터 로드
    original_file = '../data/raw/naver_ratings.csv'
    retry_file = '../data/raw/naver_ratings_retry.csv'

    try:
        original_df = pd.read_csv(original_file, encoding='utf-8-sig')
        print(f"원본 데이터: {len(original_df)}편")
    except FileNotFoundError:
        print(f"❌ 원본 파일을 찾을 수 없습니다: {original_file}")
        return

    try:
        retry_df = pd.read_csv(retry_file, encoding='utf-8-sig')
        print(f"재수집 데이터: {len(retry_df)}편")
    except FileNotFoundError:
        print(f"❌ 재수집 파일을 찾을 수 없습니다: {retry_file}")
        print("먼저 retry_missing_movies.py를 실행하세요.")
        return

    print("\n" + "="*80)

    # 2. 원본에서 누락된 영화 찾기
    important_columns = [
        'viewer_total', 'netizen_total', 'critic_rating_avg'
    ]

    original_missing = []
    for idx, row in original_df.iterrows():
        # 주요 평점이 모두 없으면 누락
        if all(pd.isna(row[col]) or row[col] == '' for col in important_columns):
            original_missing.append(row['movie_name'])

    print(f"\n원본 누락: {len(original_missing)}편")

    # 3. 재수집에서 성공한 영화 찾기
    retry_success = []
    retry_still_missing = []

    for idx, row in retry_df.iterrows():
        movie_name = row['movie_name']

        # 하나라도 수집되었으면 성공
        if any(pd.notna(row[col]) and row[col] != '' for col in important_columns):
            retry_success.append(movie_name)
        else:
            retry_still_missing.append(movie_name)

    print(f"재수집 성공: {len(retry_success)}편")
    print(f"재수집 실패: {len(retry_still_missing)}편")

    # 4. 여전히 누락된 영화 출력
    print("\n" + "="*80)
    print("\n[재수집 후에도 여전히 누락된 영화]")
    print("-"*80)

    if retry_still_missing:
        for i, movie in enumerate(retry_still_missing, 1):
            print(f"{i:2d}. {movie}")
    else:
        print("✅ 모든 영화 수집 완료!")

    print(f"\n여전히 누락: {len(retry_still_missing)}편")

    # 5. 재수집으로 복구된 영화 출력
    print("\n" + "="*80)
    print("\n[재수집으로 복구된 영화]")
    print("-"*80)

    if retry_success:
        # 재수집 데이터에서 추출 방법도 함께 출력
        for i, movie in enumerate(retry_success, 1):
            retry_row = retry_df[retry_df['movie_name'] == movie].iloc[0]

            # 수집된 항목 확인
            collected = []
            if pd.notna(retry_row['viewer_total']):
                collected.append('실관람객')
            if pd.notna(retry_row['netizen_total']):
                collected.append('네티즌')
            if pd.notna(retry_row['critic_rating_avg']):
                collected.append('평론가')

            method = retry_row.get('extraction_method', 'N/A')

            print(f"{i:2d}. {movie}")
            print(f"    수집: {', '.join(collected)} | 방법: {method}")
    else:
        print("재수집 성공한 영화가 없습니다.")

    print(f"\n재수집 성공: {len(retry_success)}편")

    # 6. 통계 요약
    print("\n" + "="*80)
    print("\n[최종 통계]")
    print("-"*80)
    print(f"원본 누락:        {len(original_missing):3d}편")
    print(f"재수집 성공:      {len(retry_success):3d}편 ({len(retry_success)/len(original_missing)*100 if original_missing else 0:5.1f}%)")
    print(f"여전히 누락:      {len(retry_still_missing):3d}편 ({len(retry_still_missing)/len(original_missing)*100 if original_missing else 0:5.1f}%)")
    print("="*80)

    # 7. 여전히 누락된 영화를 파일로 저장
    if retry_still_missing:
        still_missing_df = pd.DataFrame({
            'movie_name': retry_still_missing,
            'status': '재수집 실패'
        })

        output_file = '../data/raw/still_missing_movies.csv'
        still_missing_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ 여전히 누락된 영화 목록 저장: {output_file}")

    return {
        'original_missing': len(original_missing),
        'retry_success': len(retry_success),
        'still_missing': len(retry_still_missing),
        'still_missing_list': retry_still_missing
    }


if __name__ == '__main__':
    result = check_remaining_missing()
