"""
분석 검증 및 문제점 점검
- 통계적 유의성 검증
- 데이터 품질 확인
- 모델 성능 재평가
- 잠재적 문제점 식별
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from scipy import stats

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AnalysisValidator:
    """분석 검증 및 문제점 점검"""

    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)
        logger.info(f"데이터 로드: {len(self.df)}편")

    def check_data_quality(self):
        """데이터 품질 확인"""
        logger.info("\n" + "="*60)
        logger.info("🔍 데이터 품질 검증")
        logger.info("="*60)

        # 1. 결측치 현황
        logger.info("\n📊 결측치 현황:")
        missing_cols = ['rating', 'male_ratio', 'showTm', 'actor_star_power',
                       'director_star_power', 'total_star_power']
        for col in missing_cols:
            if col in self.df.columns:
                missing_count = self.df[col].isna().sum()
                missing_pct = missing_count / len(self.df) * 100
                logger.info(f"  {col:25s}: {missing_count:3d}개 ({missing_pct:5.1f}%)")

        # 2. 외국영화 확인
        logger.info("\n🌍 외국영화 비율:")
        if 'nations' in self.df.columns:
            korean_count = self.df[self.df['nations'].str.contains('한국', na=False)].shape[0]
            foreign_count = len(self.df) - korean_count
            logger.info(f"  한국영화: {korean_count}편 ({korean_count/len(self.df)*100:.1f}%)")
            logger.info(f"  외국영화: {foreign_count}편 ({foreign_count/len(self.df)*100:.1f}%)")

            # 외국영화 TOP 5
            foreign_movies = self.df[~self.df['nations'].str.contains('한국', na=False)]
            if len(foreign_movies) > 0:
                logger.info("\n  외국영화 TOP 5 (관객수):")
                for idx, row in foreign_movies.nlargest(5, 'audiAcc').iterrows():
                    logger.info(f"    {row['movieNm']:30s}: {row['audiAcc']:>10,d}명 ({row['nations']})")

        # 3. COVID-19 기간 영화
        logger.info("\n😷 COVID-19 기간 영화 (2020-2021):")
        covid_movies = self.df[(self.df['year'] >= 2020) & (self.df['year'] <= 2021)]
        logger.info(f"  2020-2021년 영화: {len(covid_movies)}편 ({len(covid_movies)/len(self.df)*100:.1f}%)")
        logger.info(f"  평균 관객수: {covid_movies['audiAcc'].mean():,.0f}명")
        logger.info(f"  일반 기간 평균: {self.df[~self.df.index.isin(covid_movies.index)]['audiAcc'].mean():,.0f}명")

        # 4. 재개봉 영화 확인
        logger.info("\n🔄 재개봉 영화 확인:")
        if 'openDt' in self.df.columns and 'prdtYear' in self.df.columns:
            self.df['openDt_year'] = pd.to_datetime(self.df['openDt']).dt.year
            self.df['rerelease_gap'] = self.df['openDt_year'] - self.df['prdtYear']
            rerelease = self.df[self.df['rerelease_gap'] > 1]
            logger.info(f"  재개봉 의심 영화: {len(rerelease)}편")
            if len(rerelease) > 0:
                logger.info("  재개봉 의심 영화 목록:")
                for idx, row in rerelease.head(5).iterrows():
                    logger.info(f"    {row['movieNm']:30s}: 제작년도 {int(row['prdtYear'])}, 개봉년도 {int(row['openDt_year'])}")

    def check_statistical_validity(self):
        """통계적 유의성 검증"""
        logger.info("\n" + "="*60)
        logger.info("📈 통계적 유의성 검증")
        logger.info("="*60)

        # 1. 샘플 크기
        logger.info("\n📊 샘플 크기:")
        logger.info(f"  전체: {len(self.df)}편")

        commercial = self.df[self.df['film_type'] == 'commercial']
        indie = self.df[self.df['film_type'] == 'indie']

        logger.info(f"  상업영화: {len(commercial)}편")
        logger.info(f"    성공: {commercial['success_new'].sum()}편")
        logger.info(f"    실패: {(~commercial['success_new'].astype(bool)).sum()}편")
        logger.info(f"  독립영화: {len(indie)}편")
        logger.info(f"    성공: {indie['success_new'].sum()}편")
        logger.info(f"    실패: {(~indie['success_new'].astype(bool)).sum()}편")

        # 2. 스타파워 상관관계의 통계적 유의성
        logger.info("\n⭐ 스타파워 상관관계 (p-value):")

        # 상업영화
        if len(commercial) > 0:
            corr, p_value = stats.pearsonr(
                commercial['total_star_power'].fillna(0),
                commercial['audiAcc']
            )
            logger.info(f"  상업영화 - 통합 스타파워:")
            logger.info(f"    상관계수: {corr:.3f}, p-value: {p_value:.4f} {'✅' if p_value < 0.05 else '❌'}")

        # 독립영화
        if len(indie) > 0:
            corr, p_value = stats.pearsonr(
                indie['total_star_power'].fillna(0),
                indie['audiAcc']
            )
            logger.info(f"  독립영화 - 통합 스타파워:")
            logger.info(f"    상관계수: {corr:.3f}, p-value: {p_value:.4f} {'✅' if p_value < 0.05 else '❌'}")

        # 3. 평점 역인과성 검증
        logger.info("\n📝 평점 역인과성 검증:")

        # 관객수 구간별 평점 비교
        self.df['audience_group'] = pd.cut(
            self.df['audiAcc'],
            bins=[0, 100000, 300000, 1000000, float('inf')],
            labels=['10만 미만', '10-30만', '30-100만', '100만+']
        )

        rating_by_audience = self.df.groupby('audience_group')['rating'].agg(['mean', 'count'])
        logger.info("  관객수 구간별 평균 평점:")
        for group, row in rating_by_audience.iterrows():
            if row['count'] > 0:
                logger.info(f"    {group:12s}: {row['mean']:.2f}점 ({int(row['count'])}편)")

    def check_model_issues(self):
        """모델 문제점 확인"""
        logger.info("\n" + "="*60)
        logger.info("🤖 모델 문제점 분석")
        logger.info("="*60)

        # 1. 다중공선성 확인
        logger.info("\n🔗 다중공선성 확인 (스타파워 변수):")
        star_cols = ['director_star_power', 'actor_star_power', 'total_star_power']

        if all(col in self.df.columns for col in star_cols):
            corr_matrix = self.df[star_cols].corr()
            logger.info("  상관계수 매트릭스:")
            logger.info(f"    감독-배우: {corr_matrix.loc['director_star_power', 'actor_star_power']:.3f}")
            logger.info(f"    감독-통합: {corr_matrix.loc['director_star_power', 'total_star_power']:.3f}")
            logger.info(f"    배우-통합: {corr_matrix.loc['actor_star_power', 'total_star_power']:.3f}")

            if corr_matrix.loc['actor_star_power', 'total_star_power'] > 0.8:
                logger.info("  ⚠️ 경고: 배우 스타파워와 통합 스타파워 간 높은 상관관계 (다중공선성)")

        # 2. 이상치 확인
        logger.info("\n📊 이상치 확인 (Z-score > 3):")
        numeric_cols = ['audiAcc', 'total_star_power', 'rating']

        for col in numeric_cols:
            if col in self.df.columns:
                z_scores = np.abs(stats.zscore(self.df[col].dropna()))
                outliers = (z_scores > 3).sum()
                logger.info(f"  {col:20s}: {outliers}개 이상치")

        # 3. 상업/독립 분류 경계선 영화
        logger.info("\n🎬 분류 경계선 영화 (매출 50-70억):")
        boundary_movies = self.df[
            (self.df['salesAcc'] >= 5_000_000_000) &
            (self.df['salesAcc'] <= 7_000_000_000)
        ]
        logger.info(f"  경계선 영화: {len(boundary_movies)}편")
        if len(boundary_movies) > 0:
            logger.info("  경계선 영화 샘플:")
            for idx, row in boundary_movies.head(5).iterrows():
                logger.info(f"    {row['movieNm']:30s}: {row['salesAcc']/100000000:.1f}억 ({row['film_type']})")

    def identify_critical_issues(self):
        """치명적 문제점 식별"""
        logger.info("\n" + "="*60)
        logger.info("⚠️ 치명적 문제점 및 제한사항")
        logger.info("="*60)

        issues = []

        # 1. 샘플 크기
        commercial = self.df[self.df['film_type'] == 'commercial']
        if len(commercial) < 100:
            issues.append({
                'severity': 'HIGH',
                'category': '샘플 크기',
                'issue': f'상업영화 샘플이 {len(commercial)}편으로 부족',
                'impact': '모델 과적합 위험, 일반화 성능 저하',
                'recommendation': '데이터 추가 수집 또는 통합 분석 고려'
            })

        # 2. 결측치
        rating_missing = self.df['rating'].isna().sum()
        if rating_missing > len(self.df) * 0.15:
            issues.append({
                'severity': 'MEDIUM',
                'category': '결측치',
                'issue': f'평점 결측치 {rating_missing}개 ({rating_missing/len(self.df)*100:.1f}%)',
                'impact': '평점 변수의 중요도가 왜곡될 수 있음',
                'recommendation': '결측치 처리 방법 명시 (중앙값 대체 사용)'
            })

        # 3. 외국영화
        if 'nations' in self.df.columns:
            foreign_count = len(self.df[~self.df['nations'].str.contains('한국', na=False)])
            if foreign_count > 0:
                issues.append({
                    'severity': 'HIGH',
                    'category': '데이터 구성',
                    'issue': f'외국영화 {foreign_count}편 포함',
                    'impact': '한국영화 성공 공식이 왜곡됨 (외국영화 특성 다름)',
                    'recommendation': '한국영화만 필터링하여 재분석'
                })

        # 4. COVID-19
        covid_movies = self.df[(self.df['year'] >= 2020) & (self.df['year'] <= 2021)]
        if len(covid_movies) > len(self.df) * 0.2:
            issues.append({
                'severity': 'MEDIUM',
                'category': '시기적 편향',
                'issue': f'COVID-19 기간 영화 {len(covid_movies)}편 ({len(covid_movies)/len(self.df)*100:.1f}%)',
                'impact': '2020-2021년 데이터가 비정상적으로 낮음',
                'recommendation': 'COVID 기간 별도 분석 또는 제외 고려'
            })

        # 5. 제작비 추정
        issues.append({
            'severity': 'HIGH',
            'category': '성공 기준',
            'issue': '실제 제작비 데이터 없음 (평균값으로 추정)',
            'impact': '성공/실패 분류가 부정확할 수 있음',
            'recommendation': '제작비 추정의 한계를 명시, 매출 기준으로 대체 분석'
        })

        # 6. 역인과성
        issues.append({
            'severity': 'HIGH',
            'category': '인과관계',
            'issue': '평점과 관객수의 역인과성 문제',
            'impact': '평점이 높아서 관객이 많은지, 관객이 많아서 평점이 높은지 불명확',
            'recommendation': '평점을 예측 변수가 아닌 결과 변수로 재해석'
        })

        # 7. 누락 변수
        issues.append({
            'severity': 'MEDIUM',
            'category': '누락 변수',
            'issue': '스크린 수, 마케팅 비용, 제작사 등 미포함',
            'impact': '성공 요인의 일부만 분석',
            'recommendation': '분석의 한계로 명시'
        })

        # 8. 다중공선성
        star_cols = ['actor_star_power', 'total_star_power']
        if all(col in self.df.columns for col in star_cols):
            corr = self.df[star_cols].corr().iloc[0, 1]
            if corr > 0.8:
                issues.append({
                    'severity': 'MEDIUM',
                    'category': '다중공선성',
                    'issue': f'배우 스타파워와 통합 스타파워 상관계수 {corr:.3f}',
                    'impact': '변수 중요도가 분산되어 해석이 어려움',
                    'recommendation': '하나의 스타파워 지표만 사용 권장'
                })

        # 문제점 출력
        for i, issue in enumerate(issues, 1):
            severity_emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}
            logger.info(f"\n{severity_emoji[issue['severity']]} 문제 {i}: {issue['category']}")
            logger.info(f"  내용: {issue['issue']}")
            logger.info(f"  영향: {issue['impact']}")
            logger.info(f"  권장사항: {issue['recommendation']}")

        return issues

    def generate_recommendations(self):
        """개선 권장사항"""
        logger.info("\n" + "="*60)
        logger.info("💡 개선 권장사항")
        logger.info("="*60)

        recommendations = [
            {
                'category': '데이터 정제',
                'action': '외국영화 제외 (한국영화만 분석)',
                'priority': 'HIGH',
                'reason': '한국영화와 외국영화는 성공 요인이 다름'
            },
            {
                'category': '데이터 정제',
                'action': 'COVID-19 기간 별도 분석 또는 가중치 적용',
                'priority': 'MEDIUM',
                'reason': '2020-2021년 데이터가 비정상적'
            },
            {
                'category': '변수 선택',
                'action': '평점을 예측 변수에서 제외',
                'priority': 'HIGH',
                'reason': '역인과성 문제 (관객이 많으면 평점도 높음)'
            },
            {
                'category': '변수 선택',
                'action': '통합 스타파워만 사용 (감독/배우 개별 제거)',
                'priority': 'MEDIUM',
                'reason': '다중공선성 문제 해결'
            },
            {
                'category': '모델링',
                'action': '회귀 모델 결과 제외 또는 재학습',
                'priority': 'HIGH',
                'reason': 'R² 음수는 사용 불가'
            },
            {
                'category': '성공 기준',
                'action': '다양한 성공 기준으로 민감도 분석',
                'priority': 'MEDIUM',
                'reason': '제작비 추정의 불확실성'
            },
            {
                'category': '발표 전략',
                'action': '분석의 한계를 명시',
                'priority': 'HIGH',
                'reason': '학술적 정직성과 신뢰도 확보'
            }
        ]

        for i, rec in enumerate(recommendations, 1):
            priority_emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}
            logger.info(f"\n{priority_emoji[rec['priority']]} 권장사항 {i}: {rec['category']}")
            logger.info(f"  조치: {rec['action']}")
            logger.info(f"  이유: {rec['reason']}")


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent
    data_path = base_path / 'data' / 'processed' / 'final_dataset_with_types.csv'

    logger.info("="*60)
    logger.info("🔍 분석 검증 및 문제점 점검")
    logger.info("="*60)

    validator = AnalysisValidator(str(data_path))

    # 데이터 품질 확인
    validator.check_data_quality()

    # 통계적 유의성 검증
    validator.check_statistical_validity()

    # 모델 문제점 확인
    validator.check_model_issues()

    # 치명적 문제점 식별
    validator.identify_critical_issues()

    # 개선 권장사항
    validator.generate_recommendations()

    logger.info("\n" + "="*60)
    logger.info("✅ 검증 완료!")
    logger.info("="*60)


if __name__ == '__main__':
    main()
