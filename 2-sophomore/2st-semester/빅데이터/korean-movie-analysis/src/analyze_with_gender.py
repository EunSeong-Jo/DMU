"""
성별 및 평점 포함 종합 분석
- 상업 vs 독립 영화 성공 요인
- 성별 선호도와 흥행의 관계
- Random Forest로 중요 변수 파악
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def analyze_gender_impact():
    """성별 및 평점이 흥행에 미치는 영향 분석"""

    base_path = Path(__file__).parent.parent

    # 1. 데이터 로드
    logger.info("\n" + "=" * 80)
    logger.info("📂 최종 데이터 로드...")
    logger.info("=" * 80)

    data_file = base_path / 'data' / 'processed' / 'korean_movies_final.csv'
    df = pd.read_csv(data_file, encoding='utf-8-sig')

    logger.info(f"  총 영화: {len(df)}편")
    logger.info(f"  성공 영화: {df['success'].sum()}편 ({df['success'].mean()*100:.1f}%)")

    # 2. 성별 선호도와 성공의 관계
    logger.info("\n" + "=" * 80)
    logger.info("🎭 성별 선호도 분석")
    logger.info("=" * 80)

    # 성별 선호 영화 분류
    df_with_gender = df[df['viewer_gender_gap'].notna()].copy()

    male_preferred = df_with_gender[df_with_gender['viewer_gender_gap'] > 0.1]
    female_preferred = df_with_gender[df_with_gender['viewer_gender_gap'] < -0.1]
    neutral = df_with_gender[df_with_gender['viewer_gender_gap'].abs() <= 0.1]

    logger.info(f"\n  [성별 선호도별 분류]")
    logger.info(f"  남성 선호: {len(male_preferred)}편")
    logger.info(f"  여성 선호: {len(female_preferred)}편")
    logger.info(f"  중립: {len(neutral)}편")

    # 성별 선호도별 성공률
    male_success_rate = male_preferred['success'].mean() * 100
    female_success_rate = female_preferred['success'].mean() * 100
    neutral_success_rate = neutral['success'].mean() * 100

    logger.info(f"\n  [성별 선호도별 성공률]")
    logger.info(f"  남성 선호 영화: {male_success_rate:.1f}%")
    logger.info(f"  여성 선호 영화: {female_success_rate:.1f}%")
    logger.info(f"  중립 영화: {neutral_success_rate:.1f}%")

    # 통계적 검정
    if len(male_preferred) > 10 and len(female_preferred) > 10:
        stat, p_value = stats.chi2_contingency([
            [male_preferred['success'].sum(), len(male_preferred) - male_preferred['success'].sum()],
            [female_preferred['success'].sum(), len(female_preferred) - female_preferred['success'].sum()]
        ])[:2]

        logger.info(f"\n  [카이제곱 검정: 남성 선호 vs 여성 선호]")
        logger.info(f"  p-value: {p_value:.4f}")
        if p_value < 0.05:
            logger.info(f"  ✅ 통계적으로 유의미한 차이 있음 (p<0.05)")
        else:
            logger.info(f"  ❌ 통계적으로 유의미한 차이 없음 (p>=0.05)")

    # 3. 평점과 성공의 관계
    logger.info("\n" + "=" * 80)
    logger.info("⭐ 평점과 성공의 관계")
    logger.info("=" * 80)

    success_movies = df[df['success'] == 1]
    fail_movies = df[df['success'] == 0]

    logger.info(f"\n  [성공 영화 vs 실패 영화 평점 비교]")

    # 실관람객 평점
    if success_movies['viewer_total'].notna().sum() > 0:
        success_viewer = success_movies['viewer_total'].mean()
        fail_viewer = fail_movies['viewer_total'].mean()

        logger.info(f"\n  실관람객 평점:")
        logger.info(f"    성공 영화: {success_viewer:.2f}")
        logger.info(f"    실패 영화: {fail_viewer:.2f}")
        logger.info(f"    차이: {success_viewer - fail_viewer:+.2f}")

        # t-test
        t_stat, p_value = stats.ttest_ind(
            success_movies['viewer_total'].dropna(),
            fail_movies['viewer_total'].dropna()
        )
        logger.info(f"    t-test p-value: {p_value:.4f}")

    # 네티즌 평점
    if success_movies['netizen_total'].notna().sum() > 0:
        success_netizen = success_movies['netizen_total'].mean()
        fail_netizen = fail_movies['netizen_total'].mean()

        logger.info(f"\n  네티즌 평점:")
        logger.info(f"    성공 영화: {success_netizen:.2f}")
        logger.info(f"    실패 영화: {fail_netizen:.2f}")
        logger.info(f"    차이: {success_netizen - fail_netizen:+.2f}")

    # 평론가 평점
    if success_movies['critic_rating_avg'].notna().sum() > 0:
        success_critic = success_movies['critic_rating_avg'].mean()
        fail_critic = fail_movies['critic_rating_avg'].mean()

        logger.info(f"\n  평론가 평점:")
        logger.info(f"    성공 영화: {success_critic:.2f}")
        logger.info(f"    실패 영화: {fail_critic:.2f}")
        logger.info(f"    차이: {success_critic - fail_critic:+.2f}")

    # 4. 상업/독립 영화별 분석
    logger.info("\n" + "=" * 80)
    logger.info("🎬 상업 vs 독립 영화 분석")
    logger.info("=" * 80)

    commercial = df[df['movie_type'] == 'commercial']
    indie = df[df['movie_type'] == 'indie']

    logger.info(f"\n  [상업 영화] {len(commercial)}편")
    logger.info(f"  평균 실관람객 평점: {commercial['viewer_total'].mean():.2f}")
    logger.info(f"  평균 여성 관객 비율: {commercial['viewer_ratio_female'].mean():.1f}%")
    logger.info(f"  성별 평점 차이 평균: {commercial['viewer_gender_gap'].mean():.2f}")

    logger.info(f"\n  [독립 영화] {len(indie)}편")
    logger.info(f"  평균 실관람객 평점: {indie['viewer_total'].mean():.2f}")
    logger.info(f"  평균 여성 관객 비율: {indie['viewer_ratio_female'].mean():.1f}%")
    logger.info(f"  성별 평점 차이 평균: {indie['viewer_gender_gap'].mean():.2f}")

    # 5. Random Forest로 변수 중요도 분석
    logger.info("\n" + "=" * 80)
    logger.info("🌲 Random Forest 변수 중요도 분석")
    logger.info("=" * 80)

    # 특징 변수 선택
    feature_cols = [
        'total_star_power', 'viewer_total', 'netizen_total', 'critic_rating_avg',
        'viewer_gender_gap_abs', 'viewer_ratio_female'
    ]

    # 결측값 없는 데이터만 선택
    df_complete = df[feature_cols + ['success']].dropna()

    logger.info(f"  분석 대상: {len(df_complete)}편 (결측값 제거 후)")

    if len(df_complete) >= 50:  # 충분한 데이터가 있을 때만 실행
        X = df_complete[feature_cols]
        y = df_complete['success']

        # 학습/테스트 분리
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Random Forest 학습
        rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
        rf.fit(X_train, y_train)

        # 정확도
        train_acc = rf.score(X_train, y_train)
        test_acc = rf.score(X_test, y_test)

        logger.info(f"\n  모델 정확도:")
        logger.info(f"    학습: {train_acc*100:.1f}%")
        logger.info(f"    테스트: {test_acc*100:.1f}%")

        # 변수 중요도
        importances = pd.DataFrame({
            '변수': feature_cols,
            '중요도': rf.feature_importances_
        }).sort_values('중요도', ascending=False)

        logger.info(f"\n  변수 중요도 순위:")
        for idx, row in importances.iterrows():
            logger.info(f"    {row['변수']:25s}: {row['중요도']:.4f}")

        # 중요도 시각화 저장
        viz_dir = base_path / 'visualizations'
        viz_dir.mkdir(exist_ok=True)

        plt.figure(figsize=(10, 6))
        plt.barh(importances['변수'], importances['중요도'])
        plt.xlabel('중요도')
        plt.title('영화 성공 예측 변수 중요도 (Random Forest)')
        plt.tight_layout()
        plt.savefig(viz_dir / 'feature_importance.png', dpi=300, bbox_inches='tight')
        logger.info(f"\n  📊 시각화 저장: {viz_dir / 'feature_importance.png'}")

    # 6. 요약 리포트 저장
    logger.info("\n" + "=" * 80)
    logger.info("📝 분석 리포트 저장")
    logger.info("=" * 80)

    report_dir = base_path / 'reports'
    report_dir.mkdir(exist_ok=True)

    report_file = report_dir / 'gender_and_rating_analysis.md'

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 성별 및 평점 포함 종합 분석 리포트\n\n")
        f.write("## 1. 데이터 개요\n\n")
        f.write(f"- 총 영화 수: {len(df)}편\n")
        f.write(f"- 성공 영화: {df['success'].sum()}편 ({df['success'].mean()*100:.1f}%)\n")
        f.write(f"- 상업 영화: {len(commercial)}편\n")
        f.write(f"- 독립 영화: {len(indie)}편\n\n")

        f.write("## 2. 성별 선호도 분석\n\n")
        f.write(f"- 남성 선호 영화: {len(male_preferred)}편 (성공률: {male_success_rate:.1f}%)\n")
        f.write(f"- 여성 선호 영화: {len(female_preferred)}편 (성공률: {female_success_rate:.1f}%)\n")
        f.write(f"- 중립 영화: {len(neutral)}편 (성공률: {neutral_success_rate:.1f}%)\n\n")

        f.write("## 3. 평점 분석\n\n")
        f.write(f"- 실관람객 평점 평균: {df['viewer_total'].mean():.2f}\n")
        f.write(f"- 네티즌 평점 평균: {df['netizen_total'].mean():.2f}\n")
        f.write(f"- 평론가 평점 평균: {df['critic_rating_avg'].mean():.2f}\n\n")

        f.write("## 4. 주요 발견사항\n\n")
        f.write(f"- 평균 성별 평점 차이: {df_with_gender['viewer_gender_gap'].mean():.2f} ")
        f.write("(음수는 여성이 더 높은 평점)\n")
        f.write(f"- 평균 여성 관객 비율: {df['viewer_ratio_female'].mean():.1f}%\n\n")

    logger.info(f"  저장 완료: {report_file}")

    logger.info("\n" + "=" * 80)
    logger.info("✅ 모든 분석 완료!")
    logger.info("=" * 80)

    return df


if __name__ == '__main__':
    df = analyze_gender_impact()
