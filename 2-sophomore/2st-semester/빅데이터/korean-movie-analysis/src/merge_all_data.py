"""
원본 데이터와 재수집 데이터를 병합하여 최종 데이터셋 생성
"""
import pandas as pd
import sys
import io

# UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def merge_all_data():
    """원본과 재수집 데이터를 병합"""

    print("="*80)
    print("데이터 병합 시작")
    print("="*80)

    # 1. 원본 데이터 로드
    original_file = '../data/raw/naver_ratings.csv'
    retry_file = '../data/raw/naver_ratings_retry.csv'

    try:
        original_df = pd.read_csv(original_file, encoding='utf-8-sig')
        print(f"\n✅ 원본 데이터 로드: {len(original_df)}편")
    except FileNotFoundError:
        print(f"❌ 원본 파일을 찾을 수 없습니다: {original_file}")
        return

    try:
        retry_df = pd.read_csv(retry_file, encoding='utf-8-sig')
        print(f"✅ 재수집 데이터 로드: {len(retry_df)}편")
    except FileNotFoundError:
        print(f"⚠️  재수집 파일이 없습니다. 원본 데이터만 사용합니다.")
        retry_df = pd.DataFrame()

    # 2. 재수집 데이터가 있으면 병합
    if not retry_df.empty:
        print(f"\n재수집 데이터 처리 중...")

        # extraction_method 컬럼 제거 (있으면)
        if 'extraction_method' in retry_df.columns:
            retry_df = retry_df.drop('extraction_method', axis=1)

        # 재수집된 영화 목록
        retry_movies = set(retry_df['movie_name'].tolist())

        # 병합 전략: 재수집 데이터로 원본 데이터 업데이트
        merged_df = original_df.copy()

        updated_count = 0
        improved_count = 0

        for idx, retry_row in retry_df.iterrows():
            movie_name = retry_row['movie_name']

            # 원본에서 해당 영화 찾기
            original_mask = merged_df['movie_name'] == movie_name

            if original_mask.any():
                original_idx = merged_df[original_mask].index[0]
                original_row = merged_df.loc[original_idx]

                # 업데이트할 컬럼들
                columns_to_update = [
                    'viewer_total', 'viewer_male', 'viewer_female',
                    'netizen_total', 'netizen_male', 'netizen_female',
                    'viewer_ratio_male', 'viewer_ratio_female',
                    'netizen_ratio_male', 'netizen_ratio_female',
                    'critic_rating_avg', 'critic_rating_count'
                ]

                # 각 컬럼별로 업데이트 필요한지 확인
                updated_columns = []

                for col in columns_to_update:
                    # 원본이 비어있고 재수집에 값이 있으면 업데이트
                    original_value = original_row[col]
                    retry_value = retry_row[col]

                    original_empty = pd.isna(original_value) or original_value == '' or original_value == 'None'
                    retry_has_value = pd.notna(retry_value) and retry_value != '' and retry_value != 'None'

                    if original_empty and retry_has_value:
                        merged_df.loc[original_idx, col] = retry_value
                        updated_columns.append(col)

                if updated_columns:
                    improved_count += 1
                    print(f"  {improved_count:2d}. {movie_name} - 업데이트: {len(updated_columns)}개 항목")

                updated_count += 1

        print(f"\n병합 완료:")
        print(f"  - 확인한 영화: {updated_count}편")
        print(f"  - 개선된 영화: {improved_count}편")

    else:
        merged_df = original_df.copy()
        print("\n재수집 데이터가 없어 원본 데이터만 사용합니다.")

    # 3. 최종 데이터 통계
    print("\n" + "="*80)
    print("최종 데이터 통계")
    print("="*80)

    important_columns = [
        'viewer_total', 'viewer_male', 'viewer_female',
        'netizen_total', 'netizen_male', 'netizen_female',
        'viewer_ratio_male', 'viewer_ratio_female',
        'netizen_ratio_male', 'netizen_ratio_female',
        'critic_rating_avg'
    ]

    # 완전한 데이터 카운트
    complete_count = 0
    partial_count = 0
    missing_count = 0

    for idx, row in merged_df.iterrows():
        missing_fields = []

        for col in important_columns:
            if pd.isna(row[col]) or row[col] == '' or row[col] == 'None':
                missing_fields.append(col)

        if len(missing_fields) == 0:
            complete_count += 1
        elif len(missing_fields) == len(important_columns):
            missing_count += 1
        else:
            partial_count += 1

    print(f"\n전체 영화:      {len(merged_df):3d}편")
    print(f"완전한 데이터:  {complete_count:3d}편 ({complete_count/len(merged_df)*100:5.1f}%)")
    print(f"부분 데이터:    {partial_count:3d}편 ({partial_count/len(merged_df)*100:5.1f}%)")
    print(f"누락 데이터:    {missing_count:3d}편 ({missing_count/len(merged_df)*100:5.1f}%)")

    # 4. 항목별 수집률
    print("\n" + "-"*80)
    print("항목별 수집률:")
    print("-"*80)

    for col in important_columns:
        collected = merged_df[col].notna().sum()
        collected -= (merged_df[col] == '').sum()
        collected -= (merged_df[col] == 'None').sum()

        rate = collected / len(merged_df) * 100
        print(f"{col:25s}: {collected:3d}개 ({rate:5.1f}%)")

    # 5. 최종 데이터 저장
    output_file = '../data/processed/naver_ratings_final.csv'

    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print("\n" + "="*80)
    print(f"✅ 최종 데이터 저장 완료: {output_file}")
    print(f"   총 {len(merged_df)}편의 영화 데이터")
    print("="*80)

    # 6. 여전히 누락된 영화 목록 저장
    still_missing = []
    for idx, row in merged_df.iterrows():
        all_missing = all(
            pd.isna(row[col]) or row[col] == '' or row[col] == 'None'
            for col in important_columns
        )
        if all_missing:
            still_missing.append(row['movie_name'])

    if still_missing:
        missing_df = pd.DataFrame({
            'movie_name': still_missing,
            'status': '데이터 없음'
        })

        missing_file = '../data/processed/final_missing_movies.csv'
        missing_df.to_csv(missing_file, index=False, encoding='utf-8-sig')

        print(f"\n⚠️  여전히 누락된 영화 {len(still_missing)}편:")
        for i, movie in enumerate(still_missing, 1):
            print(f"   {i:2d}. {movie}")
        print(f"\n   목록 저장: {missing_file}")

    return {
        'total': len(merged_df),
        'complete': complete_count,
        'partial': partial_count,
        'missing': missing_count
    }


if __name__ == '__main__':
    result = merge_all_data()

    if result:
        print(f"\n\n💾 생성된 파일:")
        print(f"   1. ../data/processed/naver_ratings_final.csv - 최종 병합 데이터")
        print(f"   2. ../data/processed/final_missing_movies.csv - 최종 누락 영화 목록")
