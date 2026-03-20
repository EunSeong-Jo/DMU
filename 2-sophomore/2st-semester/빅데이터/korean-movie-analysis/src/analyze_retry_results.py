"""
재수집 결과 분석 - 실패 및 부분 누락 항목 저장
"""
import pandas as pd
import sys
import io

# UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def analyze_retry_results():
    """재수집 결과 분석 및 저장"""

    retry_file = '../data/raw/naver_ratings_retry.csv'

    try:
        retry_df = pd.read_csv(retry_file, encoding='utf-8-sig')
        print(f"재수집 데이터 로드: {len(retry_df)}편\n")
    except FileNotFoundError:
        print(f"❌ 재수집 파일을 찾을 수 없습니다: {retry_file}")
        print("먼저 retry_missing_movies.py를 실행하세요.")
        return

    # 주요 컬럼
    rating_columns = {
        'viewer_total': '실관람객 총',
        'viewer_male': '실관람객 남',
        'viewer_female': '실관람객 여',
        'netizen_total': '네티즌 총',
        'netizen_male': '네티즌 남',
        'netizen_female': '네티즌 여',
        'viewer_ratio_male': '실관람객비율 남',
        'viewer_ratio_female': '실관람객비율 여',
        'netizen_ratio_male': '네티즌비율 남',
        'netizen_ratio_female': '네티즌비율 여',
        'critic_rating_avg': '평론가평점'
    }

    # 1. 완전 실패 (모든 항목 None)
    complete_failures = []

    # 2. 부분 성공 (일부 항목만 수집)
    partial_success = []

    for idx, row in retry_df.iterrows():
        movie_name = row['movie_name']

        # 수집된 항목과 누락된 항목 구분
        collected = []
        missing = []

        for col, name in rating_columns.items():
            if pd.notna(row[col]) and row[col] != '' and row[col] != 'None':
                collected.append(name)
            else:
                missing.append(name)

        # 모든 항목이 None이면 완전 실패
        if len(collected) == 0:
            complete_failures.append({
                'movie_name': movie_name,
                'status': '완전실패',
                'missing_items': ', '.join(missing),
                'extraction_method': row.get('extraction_method', 'N/A')
            })
        # 일부만 수집되었으면 부분 성공
        elif len(missing) > 0:
            partial_success.append({
                'movie_name': movie_name,
                'status': '부분성공',
                'collected_items': ', '.join(collected),
                'missing_items': ', '.join(missing),
                'extraction_method': row.get('extraction_method', 'N/A')
            })

    # 결과 출력
    print("="*80)
    print("\n[1] 재수집 완전 실패 (모든 항목 None)")
    print("-"*80)

    if complete_failures:
        for i, item in enumerate(complete_failures, 1):
            print(f"{i:2d}. {item['movie_name']}")
    else:
        print("없음")

    print(f"\n완전 실패: {len(complete_failures)}편")

    print("\n" + "="*80)
    print("\n[2] 재수집 부분 성공 (일부 항목만 수집)")
    print("-"*80)

    if partial_success:
        for i, item in enumerate(partial_success, 1):
            print(f"{i:2d}. {item['movie_name']}")
            print(f"    ✅ 수집: {item['collected_items']}")
            print(f"    ❌ 누락: {item['missing_items']}")
            print(f"    📌 방법: {item['extraction_method']}")
    else:
        print("없음")

    print(f"\n부분 성공: {len(partial_success)}편")

    # 통계 요약
    total_success = len(retry_df) - len(complete_failures) - len(partial_success)

    print("\n" + "="*80)
    print("\n[3] 재수집 결과 통계")
    print("-"*80)
    print(f"전체 재수집:  {len(retry_df):3d}편")
    print(f"완전 성공:    {total_success:3d}편 ({total_success/len(retry_df)*100:5.1f}%)")
    print(f"부분 성공:    {len(partial_success):3d}편 ({len(partial_success)/len(retry_df)*100:5.1f}%)")
    print(f"완전 실패:    {len(complete_failures):3d}편 ({len(complete_failures)/len(retry_df)*100:5.1f}%)")
    print("="*80)

    # CSV 파일로 저장
    import os
    os.makedirs('../data/raw', exist_ok=True)

    # 1. 완전 실패 목록 저장
    if complete_failures:
        fail_df = pd.DataFrame(complete_failures)
        fail_file = '../data/raw/retry_complete_failures.csv'
        fail_df.to_csv(fail_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ 완전 실패 목록 저장: {fail_file}")

    # 2. 부분 성공 목록 저장
    if partial_success:
        partial_df = pd.DataFrame(partial_success)
        partial_file = '../data/raw/retry_partial_success.csv'
        partial_df.to_csv(partial_file, index=False, encoding='utf-8-sig')
        print(f"✅ 부분 성공 목록 저장: {partial_file}")

    # 3. 항목별 누락 통계
    print("\n" + "="*80)
    print("\n[4] 항목별 누락 통계")
    print("-"*80)

    missing_stats = {}
    for col, name in rating_columns.items():
        missing_count = retry_df[col].isna().sum()
        missing_count += (retry_df[col] == '').sum()
        missing_count += (retry_df[col] == 'None').sum()

        if missing_count > 0:
            missing_stats[name] = missing_count
            print(f"{name:20s}: {missing_count:3d}개 누락 ({missing_count/len(retry_df)*100:5.1f}%)")

    if not missing_stats:
        print("✅ 모든 항목이 완전히 수집되었습니다!")

    # 4. 항목별 누락 통계를 CSV로 저장
    if missing_stats:
        stats_df = pd.DataFrame([
            {'item': k, 'missing_count': v, 'missing_rate': f"{v/len(retry_df)*100:.1f}%"}
            for k, v in missing_stats.items()
        ])
        stats_file = '../data/raw/retry_missing_stats.csv'
        stats_df.to_csv(stats_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ 항목별 통계 저장: {stats_file}")

    print("\n" + "="*80)

    return {
        'total': len(retry_df),
        'complete_success': total_success,
        'partial_success': len(partial_success),
        'complete_failures': len(complete_failures)
    }


if __name__ == '__main__':
    result = analyze_retry_results()

    if result:
        print("\n\n💾 저장된 파일:")
        print("  1. retry_complete_failures.csv - 재수집 완전 실패 목록")
        print("  2. retry_partial_success.csv - 재수집 부분 성공 목록")
        print("  3. retry_missing_stats.csv - 항목별 누락 통계")
