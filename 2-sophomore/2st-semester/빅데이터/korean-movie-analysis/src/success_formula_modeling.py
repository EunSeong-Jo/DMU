"""
한국 영화 성공 공식 모델링
- Random Forest로 변수 중요도 분석
- 6가지 가설 + 스타파워 통합 분석
- 성공 예측 모델 구축
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, r2_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SuccessFormulaModeler:
    """한국 영화 성공 공식 모델러"""

    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)
        self.label_encoders = {}
        logger.info(f"데이터 로드: {len(self.df)}편")

    def prepare_features(self):
        """피처 준비 및 인코딩"""
        logger.info("\n" + "="*60)
        logger.info("🔧 피처 준비 중...")
        logger.info("="*60)

        # 결측치 처리
        self.df['rating'] = self.df['rating'].fillna(self.df['rating'].median())
        self.df['male_ratio'] = self.df['male_ratio'].fillna(50.0)
        self.df['showTm'] = self.df['showTm'].fillna(self.df['showTm'].median())

        # 범주형 변수 인코딩
        categorical_features = ['season', 'main_genre', 'watch_grade_clean',
                               'director_power_grade', 'actor_power_grade']

        for col in categorical_features:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('Unknown')
                le = LabelEncoder()
                self.df[f'{col}_encoded'] = le.fit_transform(self.df[col])
                self.label_encoders[col] = le

        # 피처 선택
        feature_columns = [
            # H1: 계절
            'season_encoded',
            # H2: 장르
            'main_genre_encoded',
            # H3: 평점 (참고용)
            'rating',
            # H4: 관람등급
            'watch_grade_clean_encoded',
            # H5: 상영시간
            'showTm',
            # H6: 성별 선호도
            'male_ratio',
            # 스타파워 (핵심!)
            'director_star_power',
            'actor_star_power',
            'total_star_power',
            # 경쟁 강도
            'competition_count',
            # 추가 파생 변수
            'month'
        ]

        # 사용 가능한 피처만 선택
        self.feature_columns = [col for col in feature_columns if col in self.df.columns]

        # 결측치 최종 처리
        for col in self.feature_columns:
            if self.df[col].isna().sum() > 0:
                if self.df[col].dtype in ['float64', 'int64']:
                    self.df[col] = self.df[col].fillna(self.df[col].median())
                else:
                    self.df[col] = self.df[col].fillna(0)

        logger.info(f"선택된 피처: {len(self.feature_columns)}개")
        for col in self.feature_columns:
            logger.info(f"  - {col}")

    def train_classification_model(self):
        """성공/실패 분류 모델 (300만 기준)"""
        logger.info("\n" + "="*60)
        logger.info("🎯 성공/실패 분류 모델 학습")
        logger.info("="*60)

        # 데이터 준비
        X = self.df[self.feature_columns]
        y = self.df['success']

        logger.info(f"학습 데이터: {len(X)}편")
        logger.info(f"성공: {y.sum()}편 ({y.sum()/len(y)*100:.1f}%)")
        logger.info(f"실패: {len(y)-y.sum()}편 ({(len(y)-y.sum())/len(y)*100:.1f}%)")

        # 학습/테스트 분할
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Random Forest 모델
        rf_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'  # 불균형 데이터 처리
        )

        rf_classifier.fit(X_train, y_train)

        # 교차 검증
        cv_scores = cross_val_score(rf_classifier, X, y, cv=5)
        logger.info(f"\n교차 검증 정확도: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

        # 테스트 성능
        y_pred = rf_classifier.predict(X_test)
        logger.info(f"테스트 정확도: {rf_classifier.score(X_test, y_test):.3f}")

        logger.info("\n분류 리포트:")
        logger.info("\n" + classification_report(y_test, y_pred,
                                                 target_names=['실패', '성공']))

        # 변수 중요도
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': rf_classifier.feature_importances_
        }).sort_values('importance', ascending=False)

        logger.info("\n🔥 변수 중요도 TOP 10:")
        for idx, row in feature_importance.head(10).iterrows():
            logger.info(f"  {row['feature']:30s}: {row['importance']:.4f} ({row['importance']*100:.1f}%)")

        return rf_classifier, feature_importance

    def train_regression_model(self):
        """관객수 예측 회귀 모델"""
        logger.info("\n" + "="*60)
        logger.info("📈 관객수 예측 회귀 모델 학습")
        logger.info("="*60)

        # 데이터 준비
        X = self.df[self.feature_columns]
        y = self.df['audiAcc']

        logger.info(f"학습 데이터: {len(X)}편")
        logger.info(f"평균 관객수: {y.mean():.0f}명")
        logger.info(f"중앙값: {y.median():.0f}명")

        # 학습/테스트 분할
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Random Forest 회귀
        rf_regressor = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )

        rf_regressor.fit(X_train, y_train)

        # 교차 검증
        cv_scores = cross_val_score(rf_regressor, X, y, cv=5,
                                    scoring='r2')
        logger.info(f"\n교차 검증 R² 점수: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

        # 테스트 성능
        y_pred = rf_regressor.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        logger.info(f"테스트 R² 점수: {r2:.3f}")
        logger.info(f"평균 절대 오차(MAE): {mae:.0f}명")

        # 변수 중요도
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': rf_regressor.feature_importances_
        }).sort_values('importance', ascending=False)

        logger.info("\n🔥 변수 중요도 TOP 10:")
        for idx, row in feature_importance.head(10).iterrows():
            logger.info(f"  {row['feature']:30s}: {row['importance']:.4f} ({row['importance']*100:.1f}%)")

        return rf_regressor, feature_importance

    def analyze_hypotheses(self):
        """6가지 가설 개별 분석"""
        logger.info("\n" + "="*60)
        logger.info("📊 6가지 가설 분석")
        logger.info("="*60)

        # H1: 계절별 평균 관객수
        logger.info("\nH1: 계절별 개봉 효과")
        season_stats = self.df.groupby('season')['audiAcc'].agg(['mean', 'median', 'count'])
        season_stats = season_stats.sort_values('mean', ascending=False)
        for season, row in season_stats.iterrows():
            logger.info(f"  {season:6s}: 평균 {row['mean']:10,.0f}명 | 중앙값 {row['median']:10,.0f}명 | {int(row['count'])}편")

        # H2: 장르별 평균 관객수
        logger.info("\nH2: 장르별 성공률 (TOP 5)")
        genre_stats = self.df[self.df['main_genre'] != 'Unknown'].groupby('main_genre')['audiAcc'].agg(['mean', 'median', 'count'])
        genre_stats = genre_stats[genre_stats['count'] >= 5].sort_values('mean', ascending=False)
        for genre, row in genre_stats.head(5).iterrows():
            logger.info(f"  {genre:15s}: 평균 {row['mean']:10,.0f}명 | {int(row['count'])}편")

        # H3: 평점과 관객수 상관관계
        logger.info("\nH3: 평점과 관객수 상관관계")
        corr = self.df[['rating', 'audiAcc']].corr().iloc[0, 1]
        logger.info(f"  상관계수: {corr:.3f}")

        # H4: 관람등급별 평균 관객수
        logger.info("\nH4: 관람등급별 평균 관객수")
        grade_stats = self.df.groupby('watch_grade_clean')['audiAcc'].agg(['mean', 'count'])
        grade_stats = grade_stats.sort_values('mean', ascending=False)
        for grade, row in grade_stats.iterrows():
            if grade != 'Unknown':
                logger.info(f"  {grade:12s}: 평균 {row['mean']:10,.0f}명 | {int(row['count'])}편")

        # H5: 상영시간과 관객수 상관관계
        logger.info("\nH5: 상영시간과 관객수 상관관계")
        corr = self.df[['showTm', 'audiAcc']].corr().iloc[0, 1]
        logger.info(f"  상관계수: {corr:.3f}")

        # H6: 성별 비율과 관객수 상관관계
        logger.info("\nH6: 남성 비율과 관객수 상관관계")
        corr = self.df[['male_ratio', 'audiAcc']].corr().iloc[0, 1]
        logger.info(f"  상관계수: {corr:.3f}")

        # 스타파워
        logger.info("\n⭐ 스타파워와 관객수 상관관계")
        logger.info(f"  감독 스타파워: {self.df[['director_star_power', 'audiAcc']].corr().iloc[0, 1]:.3f}")
        logger.info(f"  배우 스타파워: {self.df[['actor_star_power', 'audiAcc']].corr().iloc[0, 1]:.3f}")
        logger.info(f"  통합 스타파워: {self.df[['total_star_power', 'audiAcc']].corr().iloc[0, 1]:.3f}")

    def visualize_results(self, clf_importance, reg_importance, output_dir):
        """결과 시각화"""
        logger.info("\n" + "="*60)
        logger.info("📊 결과 시각화")
        logger.info("="*60)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. 분류 모델 변수 중요도
        plt.figure(figsize=(10, 6))
        top_features = clf_importance.head(10)
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('중요도')
        plt.title('성공/실패 예측 변수 중요도 TOP 10')
        plt.tight_layout()
        plt.savefig(output_dir / 'feature_importance_classification.png', dpi=300, bbox_inches='tight')
        logger.info(f"저장: {output_dir / 'feature_importance_classification.png'}")
        plt.close()

        # 2. 회귀 모델 변수 중요도
        plt.figure(figsize=(10, 6))
        top_features = reg_importance.head(10)
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('중요도')
        plt.title('관객수 예측 변수 중요도 TOP 10')
        plt.tight_layout()
        plt.savefig(output_dir / 'feature_importance_regression.png', dpi=300, bbox_inches='tight')
        logger.info(f"저장: {output_dir / 'feature_importance_regression.png'}")
        plt.close()

        # 3. 계절별 관객수 박스플롯
        plt.figure(figsize=(10, 6))
        self.df.boxplot(column='audiAcc', by='season', figsize=(10, 6))
        plt.ylabel('관객수')
        plt.title('계절별 관객수 분포')
        plt.suptitle('')
        plt.tight_layout()
        plt.savefig(output_dir / 'season_boxplot.png', dpi=300, bbox_inches='tight')
        logger.info(f"저장: {output_dir / 'season_boxplot.png'}")
        plt.close()

        # 4. 스타파워 vs 관객수 산점도
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df['total_star_power'], self.df['audiAcc'], alpha=0.5)
        plt.xlabel('통합 스타파워')
        plt.ylabel('관객수')
        plt.title('스타파워와 관객수의 관계')

        # 추세선
        z = np.polyfit(self.df['total_star_power'], self.df['audiAcc'], 1)
        p = np.poly1d(z)
        plt.plot(self.df['total_star_power'], p(self.df['total_star_power']), "r--", alpha=0.8)

        plt.tight_layout()
        plt.savefig(output_dir / 'star_power_scatter.png', dpi=300, bbox_inches='tight')
        logger.info(f"저장: {output_dir / 'star_power_scatter.png'}")
        plt.close()


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent
    data_path = base_path / 'data' / 'processed' / 'final_analysis_dataset_2019_2024.csv'
    output_dir = base_path / 'visualizations'

    logger.info("="*60)
    logger.info("🎬 한국 영화 성공 공식 모델링 시작")
    logger.info("="*60)

    # 모델러 초기화
    modeler = SuccessFormulaModeler(str(data_path))

    # 피처 준비
    modeler.prepare_features()

    # 가설 분석
    modeler.analyze_hypotheses()

    # 분류 모델 학습
    clf_model, clf_importance = modeler.train_classification_model()

    # 회귀 모델 학습
    reg_model, reg_importance = modeler.train_regression_model()

    # 시각화
    modeler.visualize_results(clf_importance, reg_importance, output_dir)

    logger.info("\n" + "="*60)
    logger.info("✅ 성공 공식 모델링 완료!")
    logger.info("="*60)


if __name__ == '__main__':
    main()
