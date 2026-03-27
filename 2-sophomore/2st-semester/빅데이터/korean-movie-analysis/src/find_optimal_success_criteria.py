"""
성공 기준 최적화 분석
- 다양한 성공률 시나리오 테스트 (20%, 25%, 30%, 35%, 40%)
- 상업영화와 독립영화에 대한 균형잡힌 기준 제시
- 분석 가능성과 의미있는 기준 사이의 균형점 찾기
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def analyze_success_criteria_scenarios(df):
    """다양한 성공률 시나리오 분석"""

    logger.info("\n" + "="*80)
    logger.info("🎯 성공 기준 최적화 분석")
    logger.info("="*80)

    # 상업영화와 독립영화 분리
    commercial = df[df['salesAcc'] >= 6_000_000_000].copy()
    indie = df[df['salesAcc'] < 6_000_000_000].copy()

    logger.info(f"\n📊 데이터 분포:")
    logger.info(f"  상업영화: {len(commercial)}편 (87.3%)")
    logger.info(f"  독립영화: {len(indie)}편 (12.7%)")

    # 각 성공률 목표에 대한 시나리오 분석
    scenarios = []

    # 시나리오 1: 20-25% 성공률 (현재 제안)
    scenarios.append({
        'name': '시나리오 1: 엄격한 기준',
        'target_rate': '20-25%',
        'commercial_threshold': 5_000_000,  # 500만명
        'indie_threshold': 400_000,  # 40만명
        'rationale': '최상위 성공작만 선별, 명확한 성공 기준'
    })

    # 시나리오 2: 30-35% 성공률 (균형)
    scenarios.append({
        'name': '시나리오 2: 균형잡힌 기준',
        'target_rate': '30-35%',
        'commercial_threshold': 4_000_000,  # 400만명
        'indie_threshold': 350_000,  # 35만명
        'rationale': '성공작과 실패작 균형, 충분한 분석 샘플'
    })

    # 시나리오 3: 35-40% 성공률 (포괄적)
    scenarios.append({
        'name': '시나리오 3: 포괄적 기준',
        'target_rate': '35-40%',
        'commercial_threshold': 3_500_000,  # 350만명
        'indie_threshold': 300_000,  # 30만명
        'rationale': '제작비 회수 성공, 더 많은 분석 샘플'
    })

    # 시나리오 4: 전체 성공률 통일 (25%)
    scenarios.append({
        'name': '시나리오 4: 통일 기준 (25%)',
        'target_rate': '25%',
        'commercial_threshold': 4_500_000,  # 450만명
        'indie_threshold': 450_000,  # 45만명
        'rationale': '상업/독립 동일한 성공률, 공정한 비교'
    })

    # 시나리오 5: 전체 성공률 통일 (30%)
    scenarios.append({
        'name': '시나리오 5: 통일 기준 (30%)',
        'target_rate': '30%',
        'commercial_threshold': 4_000_000,  # 400만명
        'indie_threshold': 380_000,  # 38만명
        'rationale': '상업/독립 동일한 성공률, 충분한 샘플'
    })

    logger.info("\n" + "="*80)
    logger.info("📈 시나리오별 분석 결과")
    logger.info("="*80)

    results = []

    for scenario in scenarios:
        logger.info(f"\n{'='*80}")
        logger.info(f"🎬 {scenario['name']}")
        logger.info(f"{'='*80}")
        logger.info(f"  목표 성공률: {scenario['target_rate']}")
        logger.info(f"  설정 근거: {scenario['rationale']}")

        # 성공 여부 계산
        commercial_success = commercial['audiAcc'] >= scenario['commercial_threshold']
        indie_success = indie['audiAcc'] >= scenario['indie_threshold']

        commercial_success_count = commercial_success.sum()
        indie_success_count = indie_success.sum()
        total_success = commercial_success_count + indie_success_count

        commercial_rate = (commercial_success_count / len(commercial) * 100)
        indie_rate = (indie_success_count / len(indie) * 100)
        total_rate = (total_success / len(df) * 100)

        logger.info(f"\n  📊 성공률:")
        logger.info(f"    상업영화: {commercial_success_count}/{len(commercial)}편 ({commercial_rate:.1f}%)")
        logger.info(f"    독립영화: {indie_success_count}/{len(indie)}편 ({indie_rate:.1f}%)")
        logger.info(f"    전체: {total_success}/{len(df)}편 ({total_rate:.1f}%)")

        logger.info(f"\n  🎯 기준:")
        logger.info(f"    상업영화: {scenario['commercial_threshold']:,}명+ (평균 {commercial[commercial_success]['audiAcc'].mean()/1e4:.0f}만명)")
        logger.info(f"    독립영화: {scenario['indie_threshold']:,}명+ (평균 {indie[indie_success]['audiAcc'].mean()/1e4:.0f}만명)")

        # 분석 가능성 평가
        logger.info(f"\n  ✅ 분석 가능성:")

        # 1. 샘플 수 충분성
        if commercial_success_count >= 30 and indie_success_count >= 10:
            analysis_feasibility = "매우 좋음"
            logger.info(f"    샘플 수: 매우 충분 (상업 {commercial_success_count}편, 독립 {indie_success_count}편)")
        elif commercial_success_count >= 20 and indie_success_count >= 7:
            analysis_feasibility = "좋음"
            logger.info(f"    샘플 수: 충분함 (상업 {commercial_success_count}편, 독립 {indie_success_count}편)")
        elif commercial_success_count >= 15 and indie_success_count >= 5:
            analysis_feasibility = "보통"
            logger.info(f"    ⚠️ 샘플 수: 최소 기준 (상업 {commercial_success_count}편, 독립 {indie_success_count}편)")
        else:
            analysis_feasibility = "부족"
            logger.info(f"    ❌ 샘플 수: 부족 (상업 {commercial_success_count}편, 독립 {indie_success_count}편)")

        # 2. 성공 기준의 의미성
        if total_rate <= 25:
            criteria_meaning = "매우 명확"
            logger.info(f"    성공 의미: 매우 명확 (상위 {total_rate:.1f}%)")
        elif total_rate <= 35:
            criteria_meaning = "명확"
            logger.info(f"    성공 의미: 명확 (상위 {total_rate:.1f}%)")
        elif total_rate <= 45:
            criteria_meaning = "보통"
            logger.info(f"    성공 의미: 보통 (상위 {total_rate:.1f}%)")
        else:
            criteria_meaning = "약함"
            logger.info(f"    ⚠️ 성공 의미: 약함 (상위 {total_rate:.1f}%)")

        # 3. 상업/독립 균형
        rate_diff = abs(commercial_rate - indie_rate)
        if rate_diff <= 5:
            balance = "매우 균형"
            logger.info(f"    균형성: 매우 균형잡힘 (차이 {rate_diff:.1f}%p)")
        elif rate_diff <= 10:
            balance = "균형"
            logger.info(f"    균형성: 균형잡힘 (차이 {rate_diff:.1f}%p)")
        elif rate_diff <= 20:
            balance = "보통"
            logger.info(f"    균형성: 보통 (차이 {rate_diff:.1f}%p)")
        else:
            balance = "불균형"
            logger.info(f"    ⚠️ 균형성: 불균형 (차이 {rate_diff:.1f}%p)")

        # 종합 평가
        scores = {
            '매우 좋음': 5, '좋음': 4, '보통': 3, '부족': 2, '약함': 1,
            '매우 명확': 5, '명확': 4,
            '매우 균형': 5, '균형': 4, '불균형': 2
        }

        total_score = scores.get(analysis_feasibility, 0) + scores.get(criteria_meaning, 0) + scores.get(balance, 0)

        if total_score >= 13:
            recommendation = "✅ 강력 추천"
        elif total_score >= 11:
            recommendation = "👍 추천"
        elif total_score >= 9:
            recommendation = "⚖️ 고려 가능"
        else:
            recommendation = "❌ 비추천"

        logger.info(f"\n  🎖️ 종합 평가: {recommendation} (점수: {total_score}/15)")

        results.append({
            'scenario': scenario['name'],
            'target_rate': scenario['target_rate'],
            'commercial_threshold': scenario['commercial_threshold'],
            'indie_threshold': scenario['indie_threshold'],
            'commercial_success': commercial_success_count,
            'indie_success': indie_success_count,
            'total_success': total_success,
            'commercial_rate': commercial_rate,
            'indie_rate': indie_rate,
            'total_rate': total_rate,
            'analysis_feasibility': analysis_feasibility,
            'criteria_meaning': criteria_meaning,
            'balance': balance,
            'total_score': total_score,
            'recommendation': recommendation
        })

    # 추천 요약
    logger.info("\n" + "="*80)
    logger.info("🏆 최종 추천 시나리오")
    logger.info("="*80)

    results_df = pd.DataFrame(results)
    best_scenario = results_df.loc[results_df['total_score'].idxmax()]

    logger.info(f"\n✅ 가장 추천하는 시나리오:")
    logger.info(f"  {best_scenario['scenario']}")
    logger.info(f"  - 상업영화: {best_scenario['commercial_threshold']:,}명+ ({best_scenario['commercial_rate']:.1f}%)")
    logger.info(f"  - 독립영화: {best_scenario['indie_threshold']:,}명+ ({best_scenario['indie_rate']:.1f}%)")
    logger.info(f"  - 전체 성공률: {best_scenario['total_rate']:.1f}%")
    logger.info(f"  - 성공 영화: {int(best_scenario['total_success'])}편")

    # 대안 시나리오
    alternatives = results_df[results_df['total_score'] >= 11].sort_values('total_score', ascending=False)

    if len(alternatives) > 1:
        logger.info(f"\n👍 대안 시나리오:")
        for idx, row in alternatives.iloc[1:].iterrows():
            logger.info(f"\n  {row['scenario']}")
            logger.info(f"    - 상업영화: {row['commercial_threshold']:,}명+ ({row['commercial_rate']:.1f}%)")
            logger.info(f"    - 독립영화: {row['indie_threshold']:,}명+ ({row['indie_rate']:.1f}%)")
            logger.info(f"    - 전체 성공률: {row['total_rate']:.1f}%")

    return results_df


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent

    data_path = base_path / 'data' / 'processed' / 'korean_movies_with_star_power.csv'

    logger.info("\n" + "="*80)
    logger.info("🎬 성공 기준 최적화 분석")
    logger.info("="*80)
    logger.info(f"  데이터: {data_path}\n")

    # 데이터 로딩
    df = pd.read_csv(data_path)

    # 시나리오 분석
    results = analyze_success_criteria_scenarios(df)

    # 결과 저장
    output_path = base_path / 'reports' / 'success_criteria_scenarios.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False, encoding='utf-8-sig')

    logger.info("\n" + "="*80)
    logger.info("✅ 분석 완료!")
    logger.info("="*80)
    logger.info(f"  결과 저장: {output_path}")


if __name__ == '__main__':
    main()
