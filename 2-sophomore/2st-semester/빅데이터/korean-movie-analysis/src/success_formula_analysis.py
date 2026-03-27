"""
한국영화 성공 공식 분석 (2014-2024, 220편)
- 스타파워 중심 분석
- Random Forest 변수 중요도 분석
- 평점 데이터 없이 KOBIS 데이터만 사용
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


class SuccessFormulaAnalyzer:
    """한국영화 성공 공식 분석기"""

    def __init__(self, data_path: str):
        """
        Args:
            data_path: 스타파워 포함 데이터 경로
        """
        logger.info("데이터 로딩...")
        self.df = pd.read_csv(data_path)
        logger.info(f"  데이터: {len(self.df)}편")

        self.label_encoders = {}

    def prepare_features(self):
        """피처 준비"""
        logger.info("\n피처 엔지니어링...")

        df = self.df.copy()

        # 1. 성공 여부 정의 (300만명 기준)
        df['success'] = (df['audiAcc'] >= 3_000_000).astype(int)

        # 2. 개봉 월 추출
        df['openMonth'] = pd.to_datetime(df['openDt'], format='%Y%m%d', errors='coerce').dt.month

        # 3. 시즌 분류
        def get_season(month):
            if month in [6, 7, 8]:
                return '여름'
            elif month in [12, 1, 2]:
                return '겨울'
            elif month in [3, 4, 5]:
                return '봄'
            else:
                return '가을'

        df['season'] = df['openMonth'].apply(get_season)

        # 4. 장르 처리 (첫 번째 장르만)
        df['mainGenre'] = df['genres'].str.split(',').str[0]

        # 5. 관람등급 단순화
        df['watchGrade'] = df['watchGradeNm'].replace({
            '전체관람가': '전체',
            '12세이상관람가': '12세',
            '12세관람가': '12세',
            '15세이상관람가': '15세',
            '15세관람가': '15세',
            '청소년관람불가': '청불'
        })

        # 6. 러닝타임 범주화
        df['runtime_category'] = pd.cut(
            df['showTm'],
            bins=[0, 100, 120, 140, 300],
            labels=['단편(<100분)', '중편(100-120분)', '장편(120-140분)', '초장편(140분+)']
        )

        # 7. 카테고리 변수 인코딩
        for col in ['season', 'mainGenre', 'watchGrade', 'runtime_category']:
            if col in df.columns:
                le = LabelEncoder()
                df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le

        self.df_prepared = df

        logger.info("  성공 영화: {}편 ({:.1f}%)".format(
            df['success'].sum(),
            df['success'].mean() * 100
        ))

        return df

    def analyze_variable_importance(self):
        """변수 중요도 분석 (Random Forest)"""
        logger.info("\n" + "="*60)
        logger.info("📊 변수 중요도 분석 (Random Forest)")
        logger.info("="*60)

        df = self.df_prepared

        # 피처 선택
        feature_cols = [
            'director_star_power',
            'actor_star_power',
            'total_star_power',
            'showTm',
            'openMonth',
            'year',
            'season_encoded',
            'mainGenre_encoded',
            'watchGrade_encoded',
            'runtime_category_encoded'
        ]

        # 결측치 제거
        df_clean = df[feature_cols + ['success', 'audiAcc']].dropna()

        X = df_clean[feature_cols]
        y_class = df_clean['success']
        y_reg = df_clean['audiAcc']

        logger.info(f"  피처 개수: {len(feature_cols)}개")
        logger.info(f"  샘플 수: {len(df_clean)}개")

        # 1. 분류 모델 (성공/실패 예측)
        logger.info("\n1. 성공/실패 예측 (분류)")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_class, test_size=0.2, random_state=42, stratify=y_class
        )

        clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        clf.fit(X_train, y_train)

        train_score = clf.score(X_train, y_train)
        test_score = clf.score(X_test, y_test)

        logger.info(f"  Train 정확도: {train_score:.3f}")
        logger.info(f"  Test 정확도: {test_score:.3f}")

        # 변수 중요도
        importances_clf = pd.DataFrame({
            'feature': feature_cols,
            'importance': clf.feature_importances_
        }).sort_values('importance', ascending=False)

        logger.info("\n  변수 중요도 (TOP 5):")
        for idx, row in importances_clf.head(5).iterrows():
            logger.info(f"    {row['feature']:25s}: {row['importance']:.1%}")

        # 2. 회귀 모델 (관객수 예측)
        logger.info("\n2. 관객수 예측 (회귀)")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_reg, test_size=0.2, random_state=42
        )

        reg = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        reg.fit(X_train, y_train)

        train_score = reg.score(X_train, y_train)
        test_score = reg.score(X_test, y_test)

        logger.info(f"  Train R²: {train_score:.3f}")
        logger.info(f"  Test R²: {test_score:.3f}")

        # 변수 중요도
        importances_reg = pd.DataFrame({
            'feature': feature_cols,
            'importance': reg.feature_importances_
        }).sort_values('importance', ascending=False)

        logger.info("\n  변수 중요도 (TOP 5):")
        for idx, row in importances_reg.head(5).iterrows():
            logger.info(f"    {row['feature']:25s}: {row['importance']:.1%}")

        return importances_clf, importances_reg

    def analyze_correlations(self):
        """상관관계 분석"""
        logger.info("\n" + "="*60)
        logger.info("📈 주요 변수 상관관계")
        logger.info("="*60)

        df = self.df_prepared

        # 스타파워와 관객수
        logger.info("\n1. 스타파워 vs 관객수:")
        corr_director = df['director_star_power'].corr(df['audiAcc'])
        corr_actor = df['actor_star_power'].corr(df['audiAcc'])
        corr_total = df['total_star_power'].corr(df['audiAcc'])

        logger.info(f"  감독 스타파워: {corr_director:.3f}")
        logger.info(f"  배우 스타파워: {corr_actor:.3f}")
        logger.info(f"  총 스타파워:   {corr_total:.3f}")

        # 러닝타임과 관객수
        logger.info("\n2. 러닝타임 vs 관객수:")
        corr_runtime = df['showTm'].corr(df['audiAcc'])
        logger.info(f"  상관계수: {corr_runtime:.3f}")

        # 개봉 월별 평균 관객수
        logger.info("\n3. 개봉 월별 평균 관객수:")
        monthly_avg = df.groupby('openMonth')['audiAcc'].mean().sort_values(ascending=False)
        for month, aud in monthly_avg.head(3).items():
            logger.info(f"  {int(month)}월: {aud:,.0f}명")

    def analyze_by_genre(self):
        """장르별 분석"""
        logger.info("\n" + "="*60)
        logger.info("🎬 장르별 분석")
        logger.info("="*60)

        df = self.df_prepared

        genre_stats = df.groupby('mainGenre').agg({
            'audiAcc': ['count', 'mean', 'median'],
            'success': 'mean'
        }).round(0)

        genre_stats.columns = ['편수', '평균관객', '중앙값', '성공률']
        genre_stats = genre_stats.sort_values('평균관객', ascending=False)

        logger.info("\n장르별 통계 (상위 10개):")
        print(genre_stats.head(10).to_string())

    def generate_report(self, output_dir: Path):
        """분석 리포트 생성"""
        logger.info("\n" + "="*60)
        logger.info("📄 분석 리포트 생성")
        logger.info("="*60)

        output_dir.mkdir(parents=True, exist_ok=True)

        df = self.df_prepared

        # 1. 기본 통계
        report = []
        report.append("=" * 60)
        report.append("한국영화 성공 공식 분석 리포트 (2014-2024)")
        report.append("=" * 60)
        report.append(f"\n총 영화 수: {len(df)}편")
        report.append(f"성공 영화: {df['success'].sum()}편 ({df['success'].mean()*100:.1f}%)")
        report.append(f"평균 관객수: {df['audiAcc'].mean():,.0f}명")
        report.append(f"중앙값: {df['audiAcc'].median():,.0f}명")

        # 2. 스타파워 통계
        report.append(f"\n\n[스타파워 통계]")
        report.append(f"감독 평균: {df['director_star_power'].mean():.2f}")
        report.append(f"배우 평균: {df['actor_star_power'].mean():.2f}")
        report.append(f"총합 평균: {df['total_star_power'].mean():.2f}")

        # 3. 상관관계
        report.append(f"\n\n[관객수 상관관계]")
        report.append(f"감독 스타파워: {df['director_star_power'].corr(df['audiAcc']):.3f}")
        report.append(f"배우 스타파워: {df['actor_star_power'].corr(df['audiAcc']):.3f}")
        report.append(f"총 스타파워:   {df['total_star_power'].corr(df['audiAcc']):.3f}")
        report.append(f"러닝타임:      {df['showTm'].corr(df['audiAcc']):.3f}")

        # 파일 저장
        report_path = output_dir / 'analysis_report.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        logger.info(f"\n  리포트 저장: {report_path}")

        return '\n'.join(report)


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent

    data_path = base_path / 'data' / 'processed' / 'korean_movies_with_star_power.csv'
    output_dir = base_path / 'reports'

    logger.info("\n" + "="*60)
    logger.info("🎬 한국영화 성공 공식 분석")
    logger.info("="*60)
    logger.info(f"  데이터: {data_path}")
    logger.info(f"  출력: {output_dir}\n")

    # 분석
    analyzer = SuccessFormulaAnalyzer(str(data_path))
    analyzer.prepare_features()
    analyzer.analyze_variable_importance()
    analyzer.analyze_correlations()
    analyzer.analyze_by_genre()
    report = analyzer.generate_report(output_dir)

    logger.info("\n" + "="*60)
    logger.info("✅ 분석 완료!")
    logger.info("="*60)


if __name__ == '__main__':
    main()
