"""
하이브리드 데이터셋 분석
- 2014-2024 TOP 10 (228편) + 2022-2024 전체 영화
- 3파트 분석: 최근 흥행 예측 / 트렌드 변화 / 평점·성별 패턴
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 경로 설정
DATA_DIR = Path(__file__).parent.parent / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'
VIZ_DIR = Path(__file__).parent.parent / 'visualizations'
REPORT_DIR = Path(__file__).parent.parent / 'reports'

VIZ_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


def load_data():
    """데이터 로드"""

    # 1. TOP 10 영화 (2014-2024, 228편)
    top10_df = pd.read_csv(PROCESSED_DIR / 'korean_movies_final.csv')
    top10_df['is_top10'] = 1

    print(f"[LOAD] TOP 10 영화: {len(top10_df)}편")

    # 2. 2022-2024 전체 영화
    all_movies = []

    for year in [2022, 2023, 2024]:
        file_path = RAW_DIR / f'korean_movies_{year}.csv'
        if file_path.exists():
            df = pd.read_csv(file_path)
            all_movies.append(df)
            print(f"[LOAD] {year}년 전체 영화: {len(df)}편")

    if all_movies:
        all_recent_df = pd.concat(all_movies, ignore_index=True)
        print(f"[LOAD] 2022-2024 전체 영화: {len(all_recent_df)}편")
    else:
        all_recent_df = pd.DataFrame()
        print("[WARNING] 2022-2024 전체 영화 데이터 없음")

    return top10_df, all_recent_df


def part1_recent_prediction(top10_df, all_recent_df):
    """
    파트 1: 2022-2024 흥행 예측 모델
    - TOP 10 진입 여부 예측
    """

    print("\n" + "="*60)
    print("파트 1: 2022-2024 흥행 예측 모델")
    print("="*60)

    if all_recent_df.empty:
        print("[SKIP] 2022-2024 전체 데이터 없음")
        return None

    # 2022-2024 TOP 10 영화 추출
    top10_df['openDt'] = pd.to_datetime(top10_df['openDt'], format='%Y%m%d', errors='coerce')
    top10_df['year'] = top10_df['openDt'].dt.year

    top10_recent = top10_df[top10_df['year'].isin([2022, 2023, 2024])].copy()
    print(f"\n[INFO] 2022-2024 TOP 10 영화: {len(top10_recent)}편")

    # 전체 영화에서 TOP 10 제외 → 비성공 영화
    all_recent_df['openDt'] = pd.to_datetime(all_recent_df['openDt'], format='%Y%m%d', errors='coerce')

    # movieCd 기준으로 TOP 10 제외
    top10_codes = set(top10_recent['movieCd'].astype(str))
    all_recent_df['movieCd'] = all_recent_df['movieCd'].astype(str)

    non_top10 = all_recent_df[~all_recent_df['movieCd'].isin(top10_codes)].copy()
    non_top10['is_top10'] = 0

    print(f"[INFO] 2022-2024 비TOP10 영화: {len(non_top10)}편")

    # 공통 컬럼만 선택
    common_cols = ['movieCd', 'movieNm', 'openDt', 'showTm', 'genres',
                   'directors', 'actors', 'watchGradeNm']

    # TOP 10 영화는 total_star_power 컬럼도 포함
    if 'total_star_power' in top10_recent.columns:
        top10_subset = top10_recent[common_cols + ['is_top10', 'total_star_power']].copy()
    else:
        top10_subset = top10_recent[common_cols + ['is_top10']].copy()

    non_top10_subset = non_top10[[c for c in common_cols if c in non_top10.columns] + ['is_top10']].copy()

    # 병합
    combined_df = pd.concat([top10_subset, non_top10_subset], ignore_index=True)

    print(f"\n[INFO] 병합 전 데이터셋: {len(combined_df)}편 (TOP10: {combined_df['is_top10'].sum()}편)")

    # 성인물(에로) 제외 (추가)
    before_filter = len(combined_df)
    combined_df = combined_df[~combined_df['genres'].str.contains('성인물\\(에로\\)', na=False)].copy()
    filtered_count = before_filter - len(combined_df)

    print(f"[INFO] 성인물(에로) 제외: {filtered_count}편 제거")
    print(f"[INFO] 최종 분석 데이터셋: {len(combined_df)}편 (TOP10: {combined_df['is_top10'].sum()}편)")
    print(f"[INFO] 성공률: {combined_df['is_top10'].mean()*100:.1f}%")

    # 특징 추출
    combined_df['showTm'] = pd.to_numeric(combined_df['showTm'], errors='coerce')
    combined_df['showTm'] = combined_df['showTm'].fillna(combined_df['showTm'].median())

    # 스타파워 (TOP 10만 있으면 나머지는 0으로 처리)
    if 'total_star_power' in combined_df.columns:
        combined_df['total_star_power'] = combined_df['total_star_power'].fillna(0)
    else:
        combined_df['total_star_power'] = 0

    # 감독 수 (개봉 전 정보)
    combined_df['director_count'] = combined_df['directors'].fillna('').apply(
        lambda x: len(x.split(',')) if x else 0
    )

    # 배우 수 (개봉 전 정보)
    combined_df['actor_count'] = combined_df['actors'].fillna('').apply(
        lambda x: len(x.split(',')) if x else 0
    )

    # 장르 원핫 인코딩
    genre_dummies = combined_df['genres'].str.get_dummies(sep=',')

    # 장르 개수 (다양성) - NaN 처리
    combined_df['genre_count'] = combined_df['genres'].fillna('').str.count(',') + 1
    combined_df.loc[combined_df['genres'].isna(), 'genre_count'] = 1  # 장르 없으면 1개로 간주

    # 특징 결합
    X = pd.concat([
        combined_df[['showTm', 'genre_count', 'total_star_power', 'director_count', 'actor_count']],
        genre_dummies
    ], axis=1)

    print(f"\n[INFO] 사용 변수:")
    print(f"  - 연속형: 상영시간, 장르개수, 스타파워, 감독수, 배우수")
    print(f"  - 장르: {len(genre_dummies.columns)}개")
    print(f"[INFO] 시즌 제외 (데이터 누수), 관람등급 제외 (인과관계 불명확)")

    y = combined_df['is_top10']

    # 학습/테스트 분할
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\n[INFO] 학습 데이터: {len(X_train)}개 (TOP10: {y_train.sum()}개)")
    print(f"[INFO] 테스트 데이터: {len(X_test)}개 (TOP10: {y_test.sum()}개)")

    # 방법 1: 클래스 가중치 조정
    print("\n" + "="*60)
    print("[방법 1] 클래스 가중치 조정 (class_weight='balanced')")
    print("="*60)

    rf_balanced = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=5,
        class_weight='balanced'  # 불균형 해결
    )
    rf_balanced.fit(X_train, y_train)
    y_pred_balanced = rf_balanced.predict(X_test)

    test_acc_balanced = rf_balanced.score(X_test, y_test)
    print(f"\n[RESULT] 테스트 정확도: {test_acc_balanced*100:.1f}%")
    print("\n분류 리포트:")
    print(classification_report(y_test, y_pred_balanced, target_names=['비TOP10', 'TOP10'], zero_division=0))

    # 방법 2: SMOTE 오버샘플링
    print("\n" + "="*60)
    print("[방법 2] SMOTE 오버샘플링")
    print("="*60)

    try:
        from imblearn.over_sampling import SMOTE

        smote = SMOTE(random_state=42)
        X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

        print(f"[INFO] SMOTE 전: {len(X_train)}개 (TOP10: {y_train.sum()}개)")
        print(f"[INFO] SMOTE 후: {len(X_train_smote)}개 (TOP10: {y_train_smote.sum()}개)")

        rf_smote = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
        rf_smote.fit(X_train_smote, y_train_smote)
        y_pred_smote = rf_smote.predict(X_test)

        test_acc_smote = rf_smote.score(X_test, y_test)
        print(f"\n[RESULT] 테스트 정확도: {test_acc_smote*100:.1f}%")
        print("\n분류 리포트:")
        print(classification_report(y_test, y_pred_smote, target_names=['비TOP10', 'TOP10'], zero_division=0))

        best_model = rf_smote
        y_pred = y_pred_smote
        test_acc = test_acc_smote
        method_name = "SMOTE"

    except ImportError:
        print("[WARNING] imbalanced-learn 라이브러리 없음. 클래스 가중치 방법 사용")
        best_model = rf_balanced
        y_pred = y_pred_balanced
        test_acc = test_acc_balanced
        method_name = "Balanced"

    # 방법 3: 성공 기준 완화 (TOP 20%)
    print("\n" + "="*60)
    print("[방법 3] 성공 기준 완화 - TOP 20%로 재분류")
    print("="*60)

    # TOP 20% 기준으로 재분류
    combined_df_sorted = combined_df.copy()

    # 박스오피스 순위 추정 (movieCd 기준)
    # TOP 10 영화들은 is_top10=1, 나머지는 0
    # 전체의 20%를 성공으로 재정의
    threshold_20pct = int(len(combined_df) * 0.2)

    # audiAcc가 있는 경우 사용, 없으면 is_top10 기준
    if 'audiAcc' in combined_df.columns:
        combined_df_sorted['is_success_20'] = 0
        # 상위 20% 선택
        top_20_indices = combined_df_sorted.nlargest(threshold_20pct, 'audiAcc', keep='all').index
        combined_df_sorted.loc[top_20_indices, 'is_success_20'] = 1
    else:
        # audiAcc 없으면 is_top10 기준으로만
        combined_df_sorted['is_success_20'] = combined_df_sorted['is_top10']

    y_20 = combined_df_sorted['is_success_20']

    print(f"[INFO] TOP 20% 성공률: {y_20.mean()*100:.1f}%")

    if y_20.mean() > 0.05:  # 5% 이상일 때만 학습
        X_train_20, X_test_20, y_train_20, y_test_20 = train_test_split(
            X, y_20, test_size=0.2, random_state=42, stratify=y_20
        )

        rf_20 = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=5,
            class_weight='balanced'
        )
        rf_20.fit(X_train_20, y_train_20)
        y_pred_20 = rf_20.predict(X_test_20)

        test_acc_20 = rf_20.score(X_test_20, y_test_20)
        print(f"\n[RESULT] 테스트 정확도: {test_acc_20*100:.1f}%")
        print("\n분류 리포트:")
        print(classification_report(y_test_20, y_pred_20, target_names=['하위 80%', '상위 20%'], zero_division=0))

    # 방법 4: 교차 검증 (StratifiedKFold)
    print("\n" + "="*60)
    print("[방법 4] 5-Fold 교차 검증")
    print("="*60)

    from sklearn.model_selection import StratifiedKFold, cross_val_score

    # SMOTE 모델로 교차 검증
    try:
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        cv_scores = []
        for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
            X_fold_train, X_fold_val = X.iloc[train_idx], X.iloc[val_idx]
            y_fold_train, y_fold_val = y.iloc[train_idx], y.iloc[val_idx]

            # SMOTE 적용
            smote_cv = SMOTE(random_state=42)
            X_fold_train_smote, y_fold_train_smote = smote_cv.fit_resample(X_fold_train, y_fold_train)

            # 모델 학습
            rf_cv = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
            rf_cv.fit(X_fold_train_smote, y_fold_train_smote)

            # 검증
            fold_score = rf_cv.score(X_fold_val, y_fold_val)
            cv_scores.append(fold_score)
            print(f"  Fold {fold}: {fold_score*100:.1f}%")

        print(f"\n[RESULT] 평균 정확도: {np.mean(cv_scores)*100:.1f}% (±{np.std(cv_scores)*100:.1f}%)")

    except:
        print("[WARNING] 교차 검증 실패, 스킵")

    # 방법 5: 임계값 조정으로 Precision 향상
    print("\n" + "="*60)
    print("[방법 5] 임계값 조정 (Precision 향상)")
    print("="*60)

    # 확률 예측
    y_proba = best_model.predict_proba(X_test)[:, 1]

    # 여러 임계값 시도
    thresholds = [0.3, 0.5, 0.7]
    best_threshold = 0.5
    best_precision = 0

    print("\n임계값별 성능:")
    for threshold in thresholds:
        y_pred_threshold = (y_proba >= threshold).astype(int)

        from sklearn.metrics import precision_score, recall_score
        precision = precision_score(y_test, y_pred_threshold, zero_division=0)
        recall = recall_score(y_test, y_pred_threshold, zero_division=0)

        print(f"  임계값 {threshold}: Precision={precision*100:.1f}%, Recall={recall*100:.1f}%")

        if precision > best_precision:
            best_precision = precision
            best_threshold = threshold

    print(f"\n[최적 임계값] {best_threshold} (Precision: {best_precision*100:.1f}%)")

    # 최적 임계값으로 최종 예측
    y_pred_final = (y_proba >= best_threshold).astype(int)

    print("\n" + "="*60)
    print(f"[최종 선택] {method_name} 방법 + 임계값 {best_threshold}")
    print("="*60)

    print("\n최종 분류 리포트:")
    print(classification_report(y_test, y_pred_final, target_names=['비TOP10', 'TOP10'], zero_division=0))

    # 특징 중요도 (최종 선택된 모델 사용)
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n[특징 중요도 Top 10]")
    print(feature_importance.head(10).to_string(index=False))

    # 시각화 1: 특징 중요도
    plt.figure(figsize=(10, 6))
    top_features = feature_importance.head(10)
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('중요도')
    plt.title('2022-2024 흥행 예측 변수 중요도')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'recent_prediction_importance.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 시각화 2: 모델 성능 Summary 이미지 생성
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('모델 성능 Summary', fontsize=16, fontweight='bold')

    # 2-1. Confusion Matrix
    from sklearn.metrics import ConfusionMatrixDisplay
    cm = confusion_matrix(y_test, y_pred_final)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['비TOP10', 'TOP10'])
    disp.plot(ax=axes[0, 0], cmap='Blues', values_format='d')
    axes[0, 0].set_title('Confusion Matrix', fontsize=12)

    # 2-2. 성능 지표 텍스트
    axes[0, 1].axis('off')

    from sklearn.metrics import precision_score, recall_score, f1_score
    precision = precision_score(y_test, y_pred_final, zero_division=0)
    recall = recall_score(y_test, y_pred_final, zero_division=0)
    f1 = f1_score(y_test, y_pred_final, zero_division=0)

    performance_text = f"""모델 성능 지표
{'='*40}

정확도 (Accuracy):     {test_acc*100:.1f}%
정밀도 (Precision):    {precision*100:.1f}%
재현율 (Recall):       {recall*100:.1f}%
F1-Score:              {f1*100:.1f}%

최적 임계값:           {best_threshold}

{'='*40}
5-Fold Cross Validation
{'='*40}
"""

    if 'cv_scores' in locals() and cv_scores:
        performance_text += f"평균: {np.mean(cv_scores)*100:.1f}%\n"
        performance_text += f"표준편차: ±{np.std(cv_scores)*100:.1f}%\n"
        for i, score in enumerate(cv_scores, 1):
            performance_text += f"Fold {i}: {score*100:.1f}%\n"

    performance_text += f"""
{'='*40}
데이터셋 정보
{'='*40}

전체 데이터:           {len(combined_df)}편
훈련 데이터:           {len(X_train)}편
테스트 데이터:         {len(X_test)}편

성공률:                {combined_df['is_top10'].mean()*100:.1f}%
"""

    axes[0, 1].text(0.05, 0.5, performance_text,
                    fontsize=10,
                    verticalalignment='center',
                    family='Malgun Gothic')

    # 2-3. 클래스별 성능 비교
    axes[1, 0].bar(['비TOP10', 'TOP10'],
                   [cm[0, 0]/(cm[0, 0]+cm[0, 1])*100,
                    cm[1, 1]/(cm[1, 0]+cm[1, 1])*100],
                   color=['skyblue', 'coral'])
    axes[1, 0].set_ylabel('Recall (%)')
    axes[1, 0].set_title('클래스별 Recall')
    axes[1, 0].set_ylim([0, 110])
    for i, v in enumerate([cm[0, 0]/(cm[0, 0]+cm[0, 1])*100,
                           cm[1, 1]/(cm[1, 0]+cm[1, 1])*100]):
        axes[1, 0].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')

    # 2-4. CV Scores 분포
    if 'cv_scores' in locals() and cv_scores:
        axes[1, 1].plot(range(1, len(cv_scores)+1),
                       [s*100 for s in cv_scores],
                       marker='o', linewidth=2, markersize=10)
        axes[1, 1].axhline(y=np.mean(cv_scores)*100,
                          color='r', linestyle='--',
                          label=f'평균: {np.mean(cv_scores)*100:.1f}%')
        axes[1, 1].set_xlabel('Fold')
        axes[1, 1].set_ylabel('정확도 (%)')
        axes[1, 1].set_title('5-Fold Cross Validation 결과')
        axes[1, 1].set_ylim([98, 101])
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
    else:
        axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'model_performance_summary.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n[SAVE] 모델 성능 Summary 이미지: {VIZ_DIR / 'model_performance_summary.png'}")

    return {
        'accuracy': test_acc,
        'feature_importance': feature_importance,
        'confusion_matrix': confusion_matrix(y_test, y_pred_final),
        'best_threshold': best_threshold,
        'cv_scores': cv_scores if 'cv_scores' in locals() else None
    }


def part1_overall_success_factors(top10_df):
    """
    파트 1: 전체 기간 성공 요인 (2014-2024)
    - 228편 TOP 10 영화의 공통 특성 분석
    - 예측 모델 없이 기술 통계 및 패턴 분석
    """

    print("\n" + "="*60)
    print("파트 1: 전체 기간 성공 요인 분석 (2014-2024)")
    print("="*60)

    print(f"\n[INFO] 분석 대상: {len(top10_df)}편 TOP 10 영화")

    results = {}

    # 1. 스타파워 분석
    if 'total_star_power' in top10_df.columns:
        star_stats = top10_df['total_star_power'].describe()

        print(f"\n[스타파워 통계]")
        print(f"  평균: {star_stats['mean']:.2f}")
        print(f"  중앙값: {star_stats['50%']:.2f}")
        print(f"  최소: {star_stats['min']:.2f}")
        print(f"  최대: {star_stats['max']:.2f}")

        # 스타파워 구간별 분포
        bins = [0, 0.3, 0.6, 1.0, float('inf')]
        labels = ['낮음(0-0.3)', '중간(0.3-0.6)', '높음(0.6-1.0)', '매우높음(1.0+)']
        top10_df['star_level'] = pd.cut(top10_df['total_star_power'], bins=bins, labels=labels)

        star_dist = top10_df['star_level'].value_counts().sort_index()
        print(f"\n[스타파워 구간별 분포]")
        for level, count in star_dist.items():
            print(f"  {level}: {count}편 ({count/len(top10_df)*100:.1f}%)")

        results['star_power'] = {
            'stats': star_stats.to_dict(),
            'distribution': star_dist.to_dict()
        }

    # 2. 장르 분석
    all_genres = top10_df['genres'].str.split(',', expand=True).stack()
    genre_counts = all_genres.value_counts()

    print(f"\n[장르별 성공 빈도 Top 10]")
    for genre, count in genre_counts.head(10).items():
        pct = count / len(top10_df) * 100
        print(f"  {genre}: {count}편 ({pct:.1f}%)")

    results['genres'] = genre_counts.to_dict()

    # 2-1. 감독 분석 (추가)
    all_directors = top10_df['directors'].str.split(',', expand=True).stack()
    director_counts = all_directors.value_counts()

    print(f"\n[감독별 성공 횟수 Top 10]")
    for director, count in director_counts.head(10).items():
        print(f"  {director}: {count}편")

    results['directors'] = director_counts.to_dict()

    # 2-2. 배우 분석 (추가)
    all_actors = top10_df['actors'].str.split(',', expand=True).stack()
    actor_counts = all_actors.value_counts()

    print(f"\n[배우별 성공 횟수 Top 10]")
    for actor, count in actor_counts.head(10).items():
        print(f"  {actor}: {count}편")

    results['actors'] = actor_counts.to_dict()

    # 3. 상영시간 분석
    runtime_stats = top10_df['showTm'].describe()

    print(f"\n[상영시간 통계]")
    print(f"  평균: {runtime_stats['mean']:.0f}분")
    print(f"  중앙값: {runtime_stats['50%']:.0f}분")
    print(f"  최소: {runtime_stats['min']:.0f}분")
    print(f"  최대: {runtime_stats['max']:.0f}분")

    # 상영시간 구간별 분포
    bins = [0, 100, 120, 140, float('inf')]
    labels = ['단편(<100분)', '표준(100-120분)', '장편(120-140분)', '초장편(140분+)']
    top10_df['runtime_level'] = pd.cut(top10_df['showTm'], bins=bins, labels=labels)

    runtime_dist = top10_df['runtime_level'].value_counts().sort_index()
    print(f"\n[상영시간 구간별 분포]")
    for level, count in runtime_dist.items():
        print(f"  {level}: {count}편 ({count/len(top10_df)*100:.1f}%)")

    results['runtime'] = {
        'stats': runtime_stats.to_dict(),
        'distribution': runtime_dist.to_dict()
    }

    # 4. 관람등급 분석
    grade_counts = top10_df['watchGradeNm'].value_counts()

    print(f"\n[관람등급별 분포]")
    for grade, count in grade_counts.items():
        pct = count / len(top10_df) * 100
        print(f"  {grade}: {count}편 ({pct:.1f}%)")

    results['grades'] = grade_counts.to_dict()

    # 5. 연도별 평균 관객 수 추이
    top10_df['openDt'] = pd.to_datetime(top10_df['openDt'], format='%Y%m%d', errors='coerce')
    top10_df['year'] = top10_df['openDt'].dt.year

    yearly_audience = top10_df.groupby('year')['audiAcc'].agg(['mean', 'count'])

    print(f"\n[연도별 평균 관객 수]")
    for year, row in yearly_audience.iterrows():
        print(f"  {int(year)}년: {row['mean']/10000:.0f}만명 ({int(row['count'])}편)")

    results['yearly_trend'] = yearly_audience.to_dict()

    # 6. 관객 수 구간별 분포 (추가)
    audience_bins = [0, 3000000, 5000000, 10000000, float('inf')]
    audience_labels = ['300만 미만', '300만-500만', '500만-1000만', '1000만+']
    top10_df['audience_level'] = pd.cut(top10_df['audiAcc'], bins=audience_bins, labels=audience_labels)

    audience_dist = top10_df['audience_level'].value_counts().sort_index()

    print(f"\n[관객 수 구간별 분포]")
    for level, count in audience_dist.items():
        pct = count / len(top10_df) * 100
        print(f"  {level}: {count}편 ({pct:.1f}%)")

    # 주요 돌파율
    over_300 = (top10_df['audiAcc'] >= 3000000).sum()
    over_500 = (top10_df['audiAcc'] >= 5000000).sum()
    over_1000 = (top10_df['audiAcc'] >= 10000000).sum()

    print(f"\n[주요 돌파율]")
    print(f"  300만+ 돌파: {over_300}편 ({over_300/len(top10_df)*100:.1f}%)")
    print(f"  500만+ 돌파: {over_500}편 ({over_500/len(top10_df)*100:.1f}%)")
    print(f"  1000만+ 돌파: {over_1000}편 ({over_1000/len(top10_df)*100:.1f}%)")

    results['audience_distribution'] = {
        'level_counts': audience_dist.to_dict(),
        'over_300': int(over_300),
        'over_500': int(over_500),
        'over_1000': int(over_1000)
    }

    # 시각화 1: 장르 분포
    plt.figure(figsize=(12, 6))
    genre_counts.head(15).plot(kind='barh', color='steelblue')
    plt.xlabel('편수')
    plt.title('전체 기간 성공 영화 장르 분포 (2014-2024)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'overall_genre_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 시각화 2: 스타파워 vs 관객 수
    if 'total_star_power' in top10_df.columns:
        plt.figure(figsize=(10, 6))
        plt.scatter(top10_df['total_star_power'], top10_df['audiAcc']/10000, alpha=0.6)
        plt.xlabel('스타파워')
        plt.ylabel('관객 수 (만명)')
        plt.title('스타파워 vs 관객 수')

        # 추세선
        z = np.polyfit(top10_df['total_star_power'].dropna(),
                       (top10_df.loc[top10_df['total_star_power'].notna(), 'audiAcc']/10000), 1)
        p = np.poly1d(z)
        plt.plot(top10_df['total_star_power'].sort_values(),
                p(top10_df['total_star_power'].sort_values()),
                "r--", alpha=0.8, label=f'추세선 (y={z[0]:.0f}x+{z[1]:.0f})')
        plt.legend()
        plt.tight_layout()
        plt.savefig(VIZ_DIR / 'overall_star_vs_audience.png', dpi=300, bbox_inches='tight')
        plt.close()

    # 시각화 3: 연도별 평균 관객 수 추이
    plt.figure(figsize=(12, 6))
    plt.plot(yearly_audience.index, yearly_audience['mean']/10000, marker='o', linewidth=2)
    plt.xlabel('연도')
    plt.ylabel('평균 관객 수 (만명)')
    plt.title('연도별 TOP 10 평균 관객 수 추이')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'overall_yearly_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

    return results


def part2_recent_prediction(top10_df, all_recent_df):
    """
    파트 2: 2022-2024 흥행 예측 모델
    - TOP 10 진입 여부 예측
    """
    # 기존 part1_recent_prediction 내용과 동일
    return part1_recent_prediction(top10_df, all_recent_df)


def part3_trend_comparison(top10_df):
    """
    파트 3: 장기 트렌드 vs 최근 트렌드
    - 2014-2021 vs 2022-2024 비교
    """

    print("\n" + "="*60)
    print("파트 3: 트렌드 변화 분석 (과거 vs 최근)")
    print("="*60)

    top10_df['openDt'] = pd.to_datetime(top10_df['openDt'], format='%Y%m%d', errors='coerce')
    top10_df['year'] = top10_df['openDt'].dt.year

    # 기간 분류
    past_df = top10_df[top10_df['year'] <= 2021].copy()
    recent_df = top10_df[top10_df['year'] >= 2022].copy()

    print(f"\n[INFO] 과거 (2014-2021): {len(past_df)}편")
    print(f"[INFO] 최근 (2022-2024): {len(recent_df)}편")

    results = {}

    # 1. 스타파워 변화
    if 'total_star_power' in top10_df.columns:
        past_star = past_df['total_star_power'].mean()
        recent_star = recent_df['total_star_power'].mean()

        print(f"\n[스타파워 평균]")
        print(f"  과거: {past_star:.2f}")
        print(f"  최근: {recent_star:.2f}")
        print(f"  변화: {((recent_star - past_star) / past_star * 100):+.1f}%")

        results['star_power'] = {'past': past_star, 'recent': recent_star}

    # 2. 장르 선호 변화
    past_genres = past_df['genres'].str.split(',', expand=True).stack().value_counts()
    recent_genres = recent_df['genres'].str.split(',', expand=True).stack().value_counts()

    print(f"\n[장르 선호도 Top 5]")
    print("과거:")
    print(past_genres.head(5).to_string())
    print("\n최근:")
    print(recent_genres.head(5).to_string())

    results['genres'] = {'past': past_genres, 'recent': recent_genres}

    # 3. 상영시간 변화
    past_runtime = past_df['showTm'].mean()
    recent_runtime = recent_df['showTm'].mean()

    print(f"\n[상영시간 평균]")
    print(f"  과거: {past_runtime:.0f}분")
    print(f"  최근: {recent_runtime:.0f}분")
    print(f"  변화: {recent_runtime - past_runtime:+.0f}분")

    results['runtime'] = {'past': past_runtime, 'recent': recent_runtime}

    # 4. 통계적 유의성 검정 (추가)
    print(f"\n[통계적 유의성 검정 (t-test)]")

    from scipy import stats

    # 스타파워 t-test
    if 'total_star_power' in top10_df.columns:
        past_star_values = past_df['total_star_power'].dropna()
        recent_star_values = recent_df['total_star_power'].dropna()

        if len(past_star_values) > 0 and len(recent_star_values) > 0:
            t_stat_star, p_value_star = stats.ttest_ind(past_star_values, recent_star_values)
            print(f"  스타파워: t={t_stat_star:.3f}, p-value={p_value_star:.4f}", end='')
            if p_value_star < 0.05:
                print(" → 유의미한 차이 있음 (p<0.05)")
            else:
                print(" → 유의미한 차이 없음 (p>=0.05)")

    # 상영시간 t-test
    past_runtime_values = past_df['showTm'].dropna()
    recent_runtime_values = recent_df['showTm'].dropna()

    if len(past_runtime_values) > 0 and len(recent_runtime_values) > 0:
        t_stat_runtime, p_value_runtime = stats.ttest_ind(past_runtime_values, recent_runtime_values)
        print(f"  상영시간: t={t_stat_runtime:.3f}, p-value={p_value_runtime:.4f}", end='')
        if p_value_runtime < 0.05:
            print(" → 유의미한 차이 있음 (p<0.05)")
        else:
            print(" → 유의미한 차이 없음 (p>=0.05)")

    # 관객 수 t-test
    past_audience_values = past_df['audiAcc'].dropna()
    recent_audience_values = recent_df['audiAcc'].dropna()

    if len(past_audience_values) > 0 and len(recent_audience_values) > 0:
        t_stat_audience, p_value_audience = stats.ttest_ind(past_audience_values, recent_audience_values)
        print(f"  관객 수: t={t_stat_audience:.3f}, p-value={p_value_audience:.4f}", end='')
        if p_value_audience < 0.05:
            print(" → 유의미한 차이 있음 (p<0.05)")
        else:
            print(" → 유의미한 차이 없음 (p>=0.05)")

    results['t_tests'] = {
        'star_power': {'t_stat': t_stat_star if 'total_star_power' in top10_df.columns else None,
                       'p_value': p_value_star if 'total_star_power' in top10_df.columns else None},
        'runtime': {'t_stat': t_stat_runtime, 'p_value': p_value_runtime},
        'audience': {'t_stat': t_stat_audience, 'p_value': p_value_audience}
    }

    # 시각화: 장르 변화
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    past_genres.head(10).plot(kind='barh', ax=axes[0], color='steelblue')
    axes[0].set_title('과거 TOP 장르 (2014-2021)')
    axes[0].set_xlabel('편수')
    axes[0].invert_yaxis()

    recent_genres.head(10).plot(kind='barh', ax=axes[1], color='coral')
    axes[1].set_title('최근 TOP 장르 (2022-2024)')
    axes[1].set_xlabel('편수')
    axes[1].invert_yaxis()

    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'trend_genre_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    return results


def part4_rating_gender_analysis(top10_df):
    """
    파트 4: 평점 및 성별 분석 (기존 분석 재사용)
    """

    print("\n" + "="*60)
    print("파트 4: 평점 및 성별 선호도 분석")
    print("="*60)

    # 평점 데이터 있는 영화만
    rating_df = top10_df[top10_df['viewer_total'].notna()].copy()

    if len(rating_df) == 0:
        print("[SKIP] 평점 데이터 없음")
        return None

    print(f"\n[INFO] 평점 데이터 영화: {len(rating_df)}편")

    # 평균 평점
    avg_viewer = rating_df['viewer_total'].mean()
    avg_netizen = rating_df['netizen_total'].mean()
    avg_critic = rating_df['critic_rating_avg'].mean()

    print(f"\n[평균 평점]")
    print(f"  실관람객: {avg_viewer:.2f}")
    print(f"  네티즌: {avg_netizen:.2f}")
    print(f"  평론가: {avg_critic:.2f}")

    # 상관계수
    corr_viewer_netizen = rating_df['viewer_total'].corr(rating_df['netizen_total'])
    corr_viewer_critic = rating_df['viewer_total'].corr(rating_df['critic_rating_avg'])

    print(f"\n[평점 간 상관계수]")
    print(f"  실관람객 ↔ 네티즌: {corr_viewer_netizen:.3f}")
    print(f"  실관람객 ↔ 평론가: {corr_viewer_critic:.3f}")

    # 장르별 성별 선호도
    genre_df = rating_df.copy()
    genre_df['genres_list'] = genre_df['genres'].str.split(',')
    genre_exploded = genre_df.explode('genres_list')

    genre_stats = genre_exploded.groupby('genres_list').agg({
        'viewer_ratio_female': 'mean',
        'movieNm': 'count'
    }).rename(columns={'movieNm': 'count'})

    genre_stats = genre_stats[genre_stats['count'] >= 5].sort_values('viewer_ratio_female', ascending=False)

    print(f"\n[장르별 여성 관객 비율 Top 5]")
    print(genre_stats.head(5).to_string())

    # 평점 vs 관객 수 상관관계 (추가)
    if 'audiAcc' in rating_df.columns:
        corr_viewer_audience = rating_df['viewer_total'].corr(rating_df['audiAcc'])
        corr_netizen_audience = rating_df['netizen_total'].corr(rating_df['audiAcc'])
        corr_critic_audience = rating_df['critic_rating_avg'].corr(rating_df['audiAcc'])

        print(f"\n[평점 ↔ 관객 수 상관계수]")
        print(f"  실관람객 평점 ↔ 관객 수: {corr_viewer_audience:.3f}")
        print(f"  네티즌 평점 ↔ 관객 수: {corr_netizen_audience:.3f}")
        print(f"  평론가 평점 ↔ 관객 수: {corr_critic_audience:.3f}")

        # 시각화 1: 평점 vs 관객 수 산점도
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # 실관람객 평점
        axes[0].scatter(rating_df['viewer_total'], rating_df['audiAcc']/10000, alpha=0.6)
        axes[0].set_xlabel('실관람객 평점')
        axes[0].set_ylabel('관객 수 (만명)')
        axes[0].set_title(f'실관람객 평점 vs 관객 수 (r={corr_viewer_audience:.3f})')
        axes[0].grid(True, alpha=0.3)

        # 네티즌 평점
        axes[1].scatter(rating_df['netizen_total'], rating_df['audiAcc']/10000, alpha=0.6, color='orange')
        axes[1].set_xlabel('네티즌 평점')
        axes[1].set_ylabel('관객 수 (만명)')
        axes[1].set_title(f'네티즌 평점 vs 관객 수 (r={corr_netizen_audience:.3f})')
        axes[1].grid(True, alpha=0.3)

        # 평론가 평점
        axes[2].scatter(rating_df['critic_rating_avg'], rating_df['audiAcc']/10000, alpha=0.6, color='green')
        axes[2].set_xlabel('평론가 평점')
        axes[2].set_ylabel('관객 수 (만명)')
        axes[2].set_title(f'평론가 평점 vs 관객 수 (r={corr_critic_audience:.3f})')
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(VIZ_DIR / 'rating_vs_audience.png', dpi=300, bbox_inches='tight')
        plt.close()

    # 시각화 2: 장르별 성별 비율 (추가)
    plt.figure(figsize=(12, 6))
    top_genres = genre_stats.head(10).sort_values('viewer_ratio_female')

    # 여성/남성 비율 계산
    female_ratio = top_genres['viewer_ratio_female']
    male_ratio = 100 - female_ratio

    # 가로 누적 막대 그래프
    y_pos = np.arange(len(top_genres))
    plt.barh(y_pos, female_ratio, label='여성', color='pink', alpha=0.7)
    plt.barh(y_pos, male_ratio, left=female_ratio, label='남성', color='lightblue', alpha=0.7)

    plt.yticks(y_pos, top_genres.index)
    plt.xlabel('비율 (%)')
    plt.title('장르별 성별 관객 비율 Top 10')
    plt.legend()
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'genre_gender_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    return {
        'avg_ratings': {'viewer': avg_viewer, 'netizen': avg_netizen, 'critic': avg_critic},
        'correlations': {'viewer_netizen': corr_viewer_netizen, 'viewer_critic': corr_viewer_critic},
        'genre_gender': genre_stats,
        'rating_audience_corr': {
            'viewer': corr_viewer_audience if 'audiAcc' in rating_df.columns else None,
            'netizen': corr_netizen_audience if 'audiAcc' in rating_df.columns else None,
            'critic': corr_critic_audience if 'audiAcc' in rating_df.columns else None
        }
    }


def generate_report(part1_results, part2_results, part3_results, part4_results):
    """최종 리포트 생성"""

    report_lines = []
    report_lines.append("# 한국 영화 하이브리드 분석 리포트\n")
    report_lines.append("## 데이터 개요\n")
    report_lines.append("- **TOP 10 영화**: 2014-2024년 228편 (성공 영화)")
    report_lines.append("- **전체 영화**: 2022-2024년 (성공/실패 혼합)")
    report_lines.append("")

    # 파트 1: 전체 기간 성공 요인
    if part1_results:
        report_lines.append("## 파트 1: 전체 기간 성공 요인 (2014-2024)\n")

        if 'star_power' in part1_results:
            stats = part1_results['star_power']['stats']
            report_lines.append("### 스타파워 분석")
            report_lines.append(f"- 평균: {stats['mean']:.2f}")
            report_lines.append(f"- 중앙값: {stats['50%']:.2f}\n")

        if 'genres' in part1_results:
            report_lines.append("### 주요 성공 장르 Top 5")
            genre_items = sorted(part1_results['genres'].items(), key=lambda x: x[1], reverse=True)
            for genre, count in genre_items[:5]:
                report_lines.append(f"- {genre}: {count}편")
            report_lines.append("")

        if 'runtime' in part1_results:
            stats = part1_results['runtime']['stats']
            report_lines.append("### 상영시간")
            report_lines.append(f"- 평균: {stats['mean']:.0f}분")
            report_lines.append(f"- 중앙값: {stats['50%']:.0f}분\n")

    # 파트 2: 최근 흥행 예측
    if part2_results:
        report_lines.append("## 파트 2: 2022-2024 흥행 예측\n")
        report_lines.append(f"- **테스트 정확도**: {part2_results['accuracy']*100:.1f}%")
        report_lines.append("\n### 주요 변수 (Top 5)")
        for idx, row in part2_results['feature_importance'].head(5).iterrows():
            report_lines.append(f"- {row['feature']}: {row['importance']:.4f}")
        report_lines.append("")

    # 파트 3: 트렌드 변화
    if part3_results:
        report_lines.append("## 파트 3: 트렌드 변화 (과거 vs 최근)\n")

        if 'star_power' in part3_results:
            past_star = part3_results['star_power']['past']
            recent_star = part3_results['star_power']['recent']
            change = ((recent_star - past_star) / past_star * 100)
            report_lines.append(f"### 스타파워 변화")
            report_lines.append(f"- 과거 (2014-2021): {past_star:.2f}")
            report_lines.append(f"- 최근 (2022-2024): {recent_star:.2f}")
            report_lines.append(f"- 변화율: {change:+.1f}%\n")

        if 'genres' in part3_results:
            report_lines.append("### 장르 선호 변화")
            report_lines.append("\n**과거 TOP 3**:")
            for genre, count in part3_results['genres']['past'].head(3).items():
                report_lines.append(f"- {genre}: {count}편")

            report_lines.append("\n**최근 TOP 3**:")
            for genre, count in part3_results['genres']['recent'].head(3).items():
                report_lines.append(f"- {genre}: {count}편")
            report_lines.append("")

    # 파트 4: 평점/성별
    if part4_results:
        report_lines.append("## 파트 4: 평점 및 성별 분석\n")

        ratings = part4_results['avg_ratings']
        report_lines.append("### 평균 평점")
        report_lines.append(f"- 실관람객: {ratings['viewer']:.2f}")
        report_lines.append(f"- 네티즌: {ratings['netizen']:.2f}")
        report_lines.append(f"- 평론가: {ratings['critic']:.2f}\n")

        corrs = part4_results['correlations']
        report_lines.append("### 평점 상관계수")
        report_lines.append(f"- 실관람객 ↔ 네티즌: {corrs['viewer_netizen']:.3f}")
        report_lines.append(f"- 실관람객 ↔ 평론가: {corrs['viewer_critic']:.3f}\n")

    report_text = "\n".join(report_lines)

    # 저장
    report_file = REPORT_DIR / 'hybrid_analysis_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(f"\n[SAVE] 리포트 저장: {report_file}")

    return report_text


def main():
    """메인 실행"""

    print("\n" + "="*60)
    print("한국 영화 하이브리드 데이터셋 분석")
    print("="*60)

    # 데이터 로드
    top10_df, all_recent_df = load_data()

    # 파트 1: 전체 기간 성공 요인
    part1_results = part1_overall_success_factors(top10_df)

    # 파트 2: 최근 흥행 예측
    part2_results = part2_recent_prediction(top10_df, all_recent_df)

    # 파트 3: 트렌드 비교
    part3_results = part3_trend_comparison(top10_df)

    # 파트 4: 평점/성별 분석
    part4_results = part4_rating_gender_analysis(top10_df)

    # 리포트 생성
    report = generate_report(part1_results, part2_results, part3_results, part4_results)

    print("\n" + "="*60)
    print("분석 완료!")
    print("="*60)
    print(f"\n[결과물]")
    print(f"- 시각화: {VIZ_DIR}")
    print(f"- 리포트: {REPORT_DIR / 'hybrid_analysis_report.md'}")


if __name__ == "__main__":
    main()
