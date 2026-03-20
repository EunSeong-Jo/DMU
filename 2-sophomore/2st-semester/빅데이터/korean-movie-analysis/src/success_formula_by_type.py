"""
영화 타입별 성공 공식 모델링
- 상업영화 (70편): 매출 120억+ = 성공
- 독립영화 (184편): 매출 30억+ = 성공
- 각 타입별 특성에 맞는 성공 요인 분석
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, r2_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FilmTypeSuccessModeler:
    """영화 타입별 성공 공식 모델러"""

    def __init__(self, commercial_path: str, indie_path: str):
        self.commercial_df = pd.read_csv(commercial_path)
        self.indie_df = pd.read_csv(indie_path)
        self.label_encoders = {}

        logger.info(f"상업영화 데이터: {len(self.commercial_df)}편")
        logger.info(f"독립영화 데이터: {len(self.indie_df)}편")

    def prepare_features(self, df, film_type):
        """피처 준비"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🔧 {film_type} 피처 준비")
        logger.info(f"{'='*60}")

        # 결측치 처리
        df['rating'] = df['rating'].fillna(df['rating'].median())
        df['male_ratio'] = df['male_ratio'].fillna(50.0)
        df['showTm'] = df['showTm'].fillna(df['showTm'].median())

        # 범주형 변수 인코딩
        categorical_features = ['season', 'main_genre', 'watch_grade_clean']

        for col in categorical_features:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown')
                le = LabelEncoder()
                df[f'{col}_encoded'] = le.fit_transform(df[col])
                self.label_encoders[f'{film_type}_{col}'] = le

        # 피처 선택
        feature_columns = [
            'season_encoded',
            'main_genre_encoded',
            'rating',
            'watch_grade_clean_encoded',
            'showTm',
            'male_ratio',
            'director_star_power',
            'actor_star_power',
            'total_star_power',
            'competition_count',
            'month'
        ]

        # 사용 가능한 피처만 선택
        available_features = [col for col in feature_columns if col in df.columns]

        # 결측치 최종 처리
        for col in available_features:
            if df[col].isna().sum() > 0:
                if df[col].dtype in ['float64', 'int64']:
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna(0)

        logger.info(f"선택된 피처: {len(available_features)}개")

        return df, available_features

    def train_model(self, df, feature_columns, film_type, target_col='success_new'):
        """모델 학습"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🎯 {film_type} 성공 예측 모델 학습")
        logger.info(f"{'='*60}")

        # 데이터 준비
        X = df[feature_columns]
        y = df[target_col]

        logger.info(f"\n학습 데이터: {len(X)}편")
        logger.info(f"성공: {y.sum()}편 ({y.sum()/len(y)*100:.1f}%)")
        logger.info(f"실패: {len(y)-y.sum()}편 ({(len(y)-y.sum())/len(y)*100:.1f}%)")

        # 학습/테스트 분할 (데이터가 적으므로 stratify 적용)
        test_size = 0.2 if len(X) >= 50 else 0.25
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Random Forest 분류 모델
        rf_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )

        rf_classifier.fit(X_train, y_train)

        # 교차 검증 (데이터 적으면 3-fold)
        cv_folds = 3 if len(X) < 100 else 5
        cv_scores = cross_val_score(rf_classifier, X, y, cv=cv_folds)
        logger.info(f"\n교차 검증 정확도 ({cv_folds}-fold): {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

        # 테스트 성능
        y_pred = rf_classifier.predict(X_test)
        logger.info(f"테스트 정확도: {rf_classifier.score(X_test, y_test):.3f}")

        logger.info("\n분류 리포트:")
        logger.info("\n" + classification_report(y_test, y_pred, target_names=['실패', '성공'], zero_division=0))

        # 변수 중요도
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': rf_classifier.feature_importances_
        }).sort_values('importance', ascending=False)

        logger.info("\n🔥 변수 중요도 TOP 10:")
        for idx, row in feature_importance.head(10).iterrows():
            logger.info(f"  {row['feature']:30s}: {row['importance']:.4f} ({row['importance']*100:.1f}%)")

        return rf_classifier, feature_importance

    def train_regression_model(self, df, feature_columns, film_type):
        """관객수 예측 회귀 모델"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📈 {film_type} 관객수 예측 회귀 모델")
        logger.info(f"{'='*60}")

        X = df[feature_columns]
        y = df['audiAcc']

        logger.info(f"\n학습 데이터: {len(X)}편")
        logger.info(f"평균 관객수: {y.mean():,.0f}명")
        logger.info(f"중앙값: {y.median():,.0f}명")

        # 학습/테스트 분할
        test_size = 0.2 if len(X) >= 50 else 0.25
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        # Random Forest 회귀
        rf_regressor = RandomForestRegressor(
            n_estimators=100,
            max_depth=12,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )

        rf_regressor.fit(X_train, y_train)

        # 교차 검증
        cv_folds = 3 if len(X) < 100 else 5
        cv_scores = cross_val_score(rf_regressor, X, y, cv=cv_folds, scoring='r2')
        logger.info(f"\n교차 검증 R² ({cv_folds}-fold): {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

        # 테스트 성능
        y_pred = rf_regressor.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        logger.info(f"테스트 R²: {r2:.3f}")
        logger.info(f"평균 절대 오차(MAE): {mae:,.0f}명")

        # 변수 중요도
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': rf_regressor.feature_importances_
        }).sort_values('importance', ascending=False)

        logger.info("\n🔥 변수 중요도 TOP 10:")
        for idx, row in feature_importance.head(10).iterrows():
            logger.info(f"  {row['feature']:30s}: {row['importance']:.4f} ({row['importance']*100:.1f}%)")

        return rf_regressor, feature_importance

    def analyze_hypotheses(self, df, film_type):
        """가설 분석"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 {film_type} 가설 분석")
        logger.info(f"{'='*60}")

        # H1: 계절
        if 'season' in df.columns:
            logger.info("\nH1: 계절별 평균 관객수")
            season_stats = df.groupby('season')['audiAcc'].agg(['mean', 'count'])
            season_stats = season_stats.sort_values('mean', ascending=False)
            for season, row in season_stats.iterrows():
                logger.info(f"  {season:6s}: {row['mean']:10,.0f}명 ({int(row['count'])}편)")

        # H2: 장르
        if 'main_genre' in df.columns:
            logger.info("\nH2: 장르별 평균 관객수 (TOP 5)")
            genre_stats = df[df['main_genre'] != 'Unknown'].groupby('main_genre')['audiAcc'].agg(['mean', 'count'])
            genre_stats = genre_stats[genre_stats['count'] >= 2].sort_values('mean', ascending=False)
            for genre, row in genre_stats.head(5).iterrows():
                logger.info(f"  {genre:15s}: {row['mean']:10,.0f}명 ({int(row['count'])}편)")

        # H3: 평점
        logger.info("\nH3: 평점과 관객수 상관관계")
        corr = df[['rating', 'audiAcc']].corr().iloc[0, 1]
        logger.info(f"  상관계수: {corr:.3f}")

        # 스타파워
        logger.info("\n⭐ 스타파워와 관객수 상관관계")
        logger.info(f"  감독 스타파워: {df[['director_star_power', 'audiAcc']].corr().iloc[0, 1]:.3f}")
        logger.info(f"  배우 스타파워: {df[['actor_star_power', 'audiAcc']].corr().iloc[0, 1]:.3f}")
        logger.info(f"  통합 스타파워: {df[['total_star_power', 'audiAcc']].corr().iloc[0, 1]:.3f}")

    def visualize_comparison(self, commercial_importance, indie_importance, output_dir):
        """타입별 비교 시각화"""
        logger.info(f"\n{'='*60}")
        logger.info("📊 결과 시각화")
        logger.info(f"{'='*60}")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 1. 상업영화 변수 중요도
        plt.figure(figsize=(10, 6))
        top_features = commercial_importance.head(10)
        plt.barh(range(len(top_features)), top_features['importance'], color='#2E86AB')
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('중요도')
        plt.title('상업영화 성공 예측 변수 중요도 TOP 10')
        plt.tight_layout()
        save_path = output_path / 'commercial_feature_importance.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"저장: {save_path}")
        plt.close()

        # 2. 독립영화 변수 중요도
        plt.figure(figsize=(10, 6))
        top_features = indie_importance.head(10)
        plt.barh(range(len(top_features)), top_features['importance'], color='#A23B72')
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('중요도')
        plt.title('독립영화 성공 예측 변수 중요도 TOP 10')
        plt.tight_layout()
        save_path = output_path / 'indie_feature_importance.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"저장: {save_path}")
        plt.close()

        # 3. 비교 차트 (TOP 5)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # 상업영화 TOP 5
        comm_top5 = commercial_importance.head(5)
        ax1.barh(range(len(comm_top5)), comm_top5['importance'], color='#2E86AB')
        ax1.set_yticks(range(len(comm_top5)))
        ax1.set_yticklabels(comm_top5['feature'])
        ax1.set_xlabel('중요도')
        ax1.set_title('상업영화 (70편)')
        ax1.invert_yaxis()

        # 독립영화 TOP 5
        indie_top5 = indie_importance.head(5)
        ax2.barh(range(len(indie_top5)), indie_top5['importance'], color='#A23B72')
        ax2.set_yticks(range(len(indie_top5)))
        ax2.set_yticklabels(indie_top5['feature'])
        ax2.set_xlabel('중요도')
        ax2.set_title('독립영화 (184편)')
        ax2.invert_yaxis()

        plt.suptitle('영화 타입별 성공 요인 비교 (TOP 5)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        save_path = output_path / 'film_type_comparison.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"저장: {save_path}")
        plt.close()


def main():
    """메인 실행"""
    base_path = Path(__file__).parent.parent
    commercial_path = base_path / 'data' / 'processed' / 'commercial_films.csv'
    indie_path = base_path / 'data' / 'processed' / 'indie_films.csv'
    output_dir = base_path / 'visualizations'

    logger.info("="*60)
    logger.info("🎬 영화 타입별 성공 공식 모델링 시작")
    logger.info("="*60)

    # 모델러 초기화
    modeler = FilmTypeSuccessModeler(str(commercial_path), str(indie_path))

    # ========== 상업영화 분석 ==========
    logger.info("\n" + "🎬"*20)
    logger.info("상업영화 분석 시작")
    logger.info("🎬"*20)

    commercial_df, commercial_features = modeler.prepare_features(
        modeler.commercial_df.copy(), "상업영화"
    )

    modeler.analyze_hypotheses(commercial_df, "상업영화")

    commercial_clf, commercial_clf_importance = modeler.train_model(
        commercial_df, commercial_features, "상업영화"
    )

    commercial_reg, commercial_reg_importance = modeler.train_regression_model(
        commercial_df, commercial_features, "상업영화"
    )

    # ========== 독립영화 분석 ==========
    logger.info("\n" + "🎥"*20)
    logger.info("독립영화 분석 시작")
    logger.info("🎥"*20)

    indie_df, indie_features = modeler.prepare_features(
        modeler.indie_df.copy(), "독립영화"
    )

    modeler.analyze_hypotheses(indie_df, "독립영화")

    indie_clf, indie_clf_importance = modeler.train_model(
        indie_df, indie_features, "독립영화"
    )

    indie_reg, indie_reg_importance = modeler.train_regression_model(
        indie_df, indie_features, "독립영화"
    )

    # ========== 비교 시각화 ==========
    modeler.visualize_comparison(
        commercial_clf_importance,
        indie_clf_importance,
        str(output_dir)
    )

    logger.info("\n" + "="*60)
    logger.info("✅ 타입별 분석 완료!")
    logger.info("="*60)


if __name__ == '__main__':
    main()
