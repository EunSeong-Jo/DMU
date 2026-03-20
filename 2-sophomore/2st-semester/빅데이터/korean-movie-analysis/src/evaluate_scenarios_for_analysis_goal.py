"""
분석 목표에 최적화된 시나리오 평가
- 목표: 전체 220편 특성 분석 + 성공 영화의 차별점 파악
- 각 시나리오가 분석 목표 달성에 얼마나 적합한지 평가
- 통계적 검정력, 효과 크기 탐지 능력, 비교 분석 가능성 평가
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from scipy import stats

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def evaluate_scenario_for_analysis(df, scenario_name, commercial_threshold, indie_threshold):
    """각 시나리오의 분석 목표 달성 가능성 평가"""

    # 상업영화와 독립영화 분리
    commercial = df[df['salesAcc'] >= 6_000_000_000].copy()
    indie = df[df['salesAcc'] < 6_000_000_000].copy()

    # 성공/실패 분류
    commercial['success'] = commercial['audiAcc'] >= commercial_threshold
    indie['success'] = indie['audiAcc'] >= indie_threshold

    df_with_success = pd.concat([commercial, indie])

    commercial_success = commercial[commercial['success']]
    commercial_fail = commercial[~commercial['success']]
    indie_success = indie[indie['success']]
    indie_fail = indie[~indie['success']]

    results = {
        'scenario': scenario_name,
        'commercial_threshold': commercial_threshold,
        'indie_threshold': indie_threshold
    }

    # 1. 샘플 크기 평가 (통계적 검정력)
    logger.info(f"\n{'='*80}")
    logger.info(f"📊 {scenario_name}")
    logger.info(f"{'='*80}")

    logger.info(f"\n1️⃣ 샘플 크기 및 통계적 검정력:")
    logger.info(f"  상업영화: 성공 {len(commercial_success)}편 vs 실패 {len(commercial_fail)}편")
    logger.info(f"  독립영화: 성공 {len(indie_success)}편 vs 실패 {len(indie_fail)}편")

    # 통계적 검정력 평가 (최소 샘플 기준)
    # t-test를 위한 최소 샘플: 각 그룹 최소 30개 권장, 최소 20개 필요
    commercial_power_score = 0
    indie_power_score = 0

    if len(commercial_success) >= 30 and len(commercial_fail) >= 30:
        commercial_power_score = 5
        commercial_power = "매우 높음 (30개+)"
    elif len(commercial_success) >= 20 and len(commercial_fail) >= 20:
        commercial_power_score = 4
        commercial_power = "높음 (20개+)"
    elif len(commercial_success) >= 15 and len(commercial_fail) >= 15:
        commercial_power_score = 3
        commercial_power = "보통 (15개+)"
    elif len(commercial_success) >= 10 and len(commercial_fail) >= 10:
        commercial_power_score = 2
        commercial_power = "낮음 (10개+)"
    else:
        commercial_power_score = 1
        commercial_power = "매우 낮음 (<10개)"

    if len(indie_success) >= 15 and len(indie_fail) >= 10:
        indie_power_score = 5
        indie_power = "매우 높음 (15개+)"
    elif len(indie_success) >= 10 and len(indie_fail) >= 8:
        indie_power_score = 4
        indie_power = "높음 (10개+)"
    elif len(indie_success) >= 7 and len(indie_fail) >= 6:
        indie_power_score = 3
        indie_power = "보통 (7개+)"
    elif len(indie_success) >= 5 and len(indie_fail) >= 5:
        indie_power_score = 2
        indie_power = "낮음 (5개+)"
    else:
        indie_power_score = 1
        indie_power = "매우 낮음 (<5개)"

    logger.info(f"  상업영화 통계적 검정력: {commercial_power}")
    logger.info(f"  독립영화 통계적 검정력: {indie_power}")

    results['commercial_power'] = commercial_power_score
    results['indie_power'] = indie_power_score

    # 2. 효과 크기 탐지 능력 (성공/실패 간 차이 검출)
    logger.info(f"\n2️⃣ 효과 크기 탐지 능력 (성공 vs 실패 차이):")

    # 주요 변수들의 효과 크기 계산 (Cohen's d)
    features = ['director_star_power', 'actor_star_power', 'total_star_power', 'showTm']

    commercial_effect_sizes = []
    indie_effect_sizes = []

    for feature in features:
        # 상업영화
        if len(commercial_success) > 0 and len(commercial_fail) > 0:
            success_mean = commercial_success[feature].mean()
            fail_mean = commercial_fail[feature].mean()
            pooled_std = np.sqrt(
                ((len(commercial_success)-1) * commercial_success[feature].std()**2 +
                 (len(commercial_fail)-1) * commercial_fail[feature].std()**2) /
                (len(commercial_success) + len(commercial_fail) - 2)
            )
            if pooled_std > 0:
                cohen_d = abs((success_mean - fail_mean) / pooled_std)
                commercial_effect_sizes.append(cohen_d)

        # 독립영화
        if len(indie_success) > 0 and len(indie_fail) > 0:
            success_mean = indie_success[feature].mean()
            fail_mean = indie_fail[feature].mean()
            pooled_std = np.sqrt(
                ((len(indie_success)-1) * indie_success[feature].std()**2 +
                 (len(indie_fail)-1) * indie_fail[feature].std()**2) /
                (len(indie_success) + len(indie_fail) - 2)
            )
            if pooled_std > 0:
                cohen_d = abs((success_mean - fail_mean) / pooled_std)
                indie_effect_sizes.append(cohen_d)

    commercial_avg_effect = np.mean(commercial_effect_sizes) if commercial_effect_sizes else 0
    indie_avg_effect = np.mean(indie_effect_sizes) if indie_effect_sizes else 0

    logger.info(f"  상업영화 평균 효과 크기 (Cohen's d): {commercial_avg_effect:.3f}")
    logger.info(f"  독립영화 평균 효과 크기 (Cohen's d): {indie_avg_effect:.3f}")

    # Cohen's d 해석: 0.2=작음, 0.5=중간, 0.8=큼
    if commercial_avg_effect >= 0.5:
        logger.info(f"  → 상업영화: 성공/실패 간 차이가 명확함 (중간 이상)")
    else:
        logger.info(f"  → 상업영화: 성공/실패 간 차이가 작음")

    if indie_avg_effect >= 0.5:
        logger.info(f"  → 독립영화: 성공/실패 간 차이가 명확함 (중간 이상)")
    else:
        logger.info(f"  → 독립영화: 성공/실패 간 차이가 작음")

    results['commercial_effect_size'] = commercial_avg_effect
    results['indie_effect_size'] = indie_avg_effect

    # 3. 전체 vs 성공 비교 분석 가능성
    logger.info(f"\n3️⃣ 전체 vs 성공 영화 비교 분석:")

    total_success = len(commercial_success) + len(indie_success)
    success_ratio = total_success / len(df) * 100

    logger.info(f"  전체 220편 중 성공: {total_success}편 ({success_ratio:.1f}%)")

    # 비교 분석 점수
    if 20 <= success_ratio <= 40:
        comparison_score = 5
        comparison_quality = "최적 (20-40%)"
        logger.info(f"  → 전체 특성 vs 성공 특성 비교에 최적")
    elif 15 <= success_ratio < 20 or 40 < success_ratio <= 50:
        comparison_score = 4
        comparison_quality = "좋음 (15-20% 또는 40-50%)"
        logger.info(f"  → 전체 특성 vs 성공 특성 비교 가능")
    elif 10 <= success_ratio < 15 or 50 < success_ratio <= 60:
        comparison_score = 3
        comparison_quality = "보통 (10-15% 또는 50-60%)"
        logger.info(f"  → 비교 가능하나 한쪽으로 치우침")
    else:
        comparison_score = 2
        comparison_quality = "불균형 (<10% 또는 >60%)"
        logger.info(f"  ⚠️ 한쪽 그룹이 너무 작거나 큼")

    results['comparison_score'] = comparison_score
    results['success_ratio'] = success_ratio

    # 4. 차별점 분석 가능성 (변수별 유의미한 차이 존재 여부)
    logger.info(f"\n4️⃣ 차별점 분석 가능성:")

    # 전체 vs 성공 영화의 차이 분석
    all_success = df_with_success[df_with_success['success']]

    significant_differences = 0
    total_tests = 0

    for feature in features:
        try:
            # t-test 수행
            stat, pval = stats.ttest_ind(
                df[feature].dropna(),
                all_success[feature].dropna(),
                equal_var=False
            )
            total_tests += 1

            if pval < 0.05:
                significant_differences += 1
                logger.info(f"  {feature}: 유의미한 차이 발견 (p={pval:.4f})")
        except:
            pass

    if total_tests > 0:
        diff_ratio = significant_differences / total_tests * 100
        logger.info(f"  → {total_tests}개 변수 중 {significant_differences}개에서 유의미한 차이 ({diff_ratio:.0f}%)")

    results['significant_diff_count'] = significant_differences
    results['significant_diff_ratio'] = diff_ratio if total_tests > 0 else 0

    # 5. Random Forest 변수 중요도 분석 가능성
    logger.info(f"\n5️⃣ Random Forest 변수 중요도 분석:")

    # 클래스 불균형 평가
    imbalance_ratio = max(total_success, len(df) - total_success) / min(total_success, len(df) - total_success)

    if imbalance_ratio <= 2:
        rf_score = 5
        rf_quality = "최적 (불균형 비율 ≤2)"
        logger.info(f"  클래스 균형: 매우 좋음 (비율 {imbalance_ratio:.2f})")
    elif imbalance_ratio <= 3:
        rf_score = 4
        rf_quality = "좋음 (불균형 비율 ≤3)"
        logger.info(f"  클래스 균형: 좋음 (비율 {imbalance_ratio:.2f})")
    elif imbalance_ratio <= 4:
        rf_score = 3
        rf_quality = "보통 (불균형 비율 ≤4)"
        logger.info(f"  클래스 균형: 보통 (비율 {imbalance_ratio:.2f})")
    else:
        rf_score = 2
        rf_quality = "불균형 (비율 >{imbalance_ratio:.0f})"
        logger.info(f"  ⚠️ 클래스 불균형 (비율 {imbalance_ratio:.2f})")

    results['rf_score'] = rf_score
    results['imbalance_ratio'] = imbalance_ratio

    # 6. 종합 점수 계산
    logger.info(f"\n6️⃣ 종합 평가 (분석 목표 달성도):")

    # 가중치 적용
    total_score = (
        commercial_power_score * 0.2 +  # 상업영화 검정력 20%
        indie_power_score * 0.15 +      # 독립영화 검정력 15%
        comparison_score * 0.25 +       # 전체 vs 성공 비교 25%
        rf_score * 0.25 +               # RF 분석 가능성 25%
        min(commercial_avg_effect, 1.0) * 5 * 0.075 +  # 상업 효과크기 7.5%
        min(indie_avg_effect, 1.0) * 5 * 0.075         # 독립 효과크기 7.5%
    )

    results['total_score'] = total_score

    logger.info(f"  통계적 검정력: {(commercial_power_score*0.2 + indie_power_score*0.15):.2f}/1.75")
    logger.info(f"  비교 분석 가능성: {comparison_score*0.25:.2f}/1.25")
    logger.info(f"  RF 분석 가능성: {rf_score*0.25:.2f}/1.25")
    logger.info(f"  효과 크기: {(min(commercial_avg_effect, 1.0)*5*0.075 + min(indie_avg_effect, 1.0)*5*0.075):.2f}/0.75")
    logger.info(f"\n  📊 종합 점수: {total_score:.2f}/5.00")

    if total_score >= 4.0:
        recommendation = "✅ 강력 추천 (분석 목표 달성에 최적)"
    elif total_score >= 3.5:
        recommendation = "👍 추천 (분석 목표 달성 가능)"
    elif total_score >= 3.0:
        recommendation = "⚖️ 고려 가능 (일부 제약 있음)"
    else:
        recommendation = "❌ 비추천 (분석 목표 달성 어려움)"

    logger.info(f"  🎖️ 최종 평가: {recommendation}")

    results['recommendation'] = recommendation

    return results


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent
    data_path = base_path / 'data' / 'processed' / 'korean_movies_with_star_power.csv'

    logger.info("\n" + "="*80)
    logger.info("🎯 분석 목표 기준 시나리오 평가")
    logger.info("="*80)
    logger.info("\n📌 분석 목표:")
    logger.info("  1. 전체 220편의 한국영화 특성 분석")
    logger.info("  2. 성공 영화가 전체 특성과 얼마나 일치하는지")
    logger.info("  3. 성공 영화의 차별점 파악")
    logger.info("  4. 각 특성이 매출(성공)에 미치는 영향도 측정\n")

    # 데이터 로딩
    df = pd.read_csv(data_path)

    # 시나리오 정의
    scenarios = [
        ("시나리오 1: 엄격한 기준 (20-25%)", 5_000_000, 400_000),
        ("시나리오 2: 균형잡힌 기준 (30-35%)", 4_000_000, 350_000),
        ("시나리오 3: 포괄적 기준 (35-40%)", 3_500_000, 300_000),
        ("시나리오 4: 통일 기준 (25%)", 4_500_000, 450_000),
        ("시나리오 5: 통일 기준 (30%)", 4_000_000, 380_000),
    ]

    results = []

    for scenario_name, commercial_threshold, indie_threshold in scenarios:
        result = evaluate_scenario_for_analysis(
            df, scenario_name, commercial_threshold, indie_threshold
        )
        results.append(result)

    # 결과 DataFrame 생성
    results_df = pd.DataFrame(results)

    # 최종 추천
    logger.info("\n" + "="*80)
    logger.info("🏆 최종 추천 (분석 목표 기준)")
    logger.info("="*80)

    best_scenario = results_df.loc[results_df['total_score'].idxmax()]

    logger.info(f"\n✅ 분석 목표 달성에 가장 적합한 시나리오:")
    logger.info(f"  {best_scenario['scenario']}")
    logger.info(f"  - 종합 점수: {best_scenario['total_score']:.2f}/5.00")
    logger.info(f"  - 전체 성공률: {best_scenario['success_ratio']:.1f}%")
    logger.info(f"  - 평가: {best_scenario['recommendation']}")

    # 상위 시나리오들 비교
    logger.info(f"\n📊 시나리오 종합 점수 비교:")
    for idx, row in results_df.sort_values('total_score', ascending=False).iterrows():
        logger.info(f"  {row['scenario']:40s} {row['total_score']:.2f}/5.00  ({row['success_ratio']:.1f}% 성공)")

    # 결과 저장
    output_path = base_path / 'reports' / 'scenario_evaluation_for_analysis.csv'
    results_df.to_csv(output_path, index=False, encoding='utf-8-sig')

    logger.info(f"\n💾 결과 저장: {output_path}")

    logger.info("\n" + "="*80)
    logger.info("✅ 평가 완료!")
    logger.info("="*80)


if __name__ == '__main__':
    main()
