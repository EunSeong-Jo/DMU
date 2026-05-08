# utils/data_loader.py
import streamlit as st
import pandas as pd
import numpy as np
import re
from pathlib import Path

# ---- 로컬 경로 ----
_DATA_DIR = Path(__file__).parent.parent / "data"
_LOCAL_CSV = _DATA_DIR / "nsmc_analyzed.csv"       # 분석 완료 결과 캐시
_RAW_TEST = _DATA_DIR / "ratings_test.txt"         # NSMC 원본 테스트 데이터

# ---- 사용할 감성 분석 모델 ----
DEFAULT_MODEL = "WhitePeak/bert-base-cased-Korean-sentiment"


# ========== 모델 로딩 ==========

@st.cache_resource(show_spinner="감성 분석 모델 로딩 중...")
def _load_sentiment_model(model_name: str):
    """HuggingFace 감성 분석 파이프라인을 로드합니다."""
    from transformers import pipeline
    import torch

    device = 0 if torch.cuda.is_available() else -1
    return pipeline(
        "sentiment-analysis",
        model=model_name,
        device=device,
        truncation=True,
        max_length=512
    )


# ========== 데이터 로딩 (3단계 폴백) ==========

def _load_local_csv():
    """로컬에 저장된 분석 완료 CSV를 읽습니다."""
    df = pd.read_csv(_LOCAL_CSV, encoding="utf-8-sig")
    return df


def _load_raw_nsmc(sample_size: int):
    """NSMC 원본 데이터를 로드하고 샘플링합니다.
    1순위: 로컬 파일 (data/ratings_test.txt)
    2순위: HuggingFace datasets 라이브러리
    """
    # 1순위: 로컬 파일
    if _RAW_TEST.exists():
        df = pd.read_csv(_RAW_TEST, sep="\t")
    else:
        # 2순위: datasets 라이브러리
        from datasets import load_dataset
        ds = load_dataset("nsmc", trust_remote_code=True)
        df = ds["test"].to_pandas()

    # NaN 및 빈 문자열 제거
    df = df.dropna(subset=["document"])
    df = df[df["document"].str.strip().astype(bool)]

    # 긍정/부정 균등 샘플링 (stratified)
    sample_size_per_label = sample_size // 2
    pos = df[df["label"] == 1].sample(n=min(sample_size_per_label, len(df[df["label"] == 1])), random_state=42)
    neg = df[df["label"] == 0].sample(n=min(sample_size_per_label, len(df[df["label"] == 0])), random_state=42)
    sampled = pd.concat([pos, neg]).sample(frac=1, random_state=42).reset_index(drop=True)

    return sampled


def _generate_simulation_data():
    """네트워크/GPU 없는 환경을 위한 시뮬레이션 데이터를 생성합니다."""
    np.random.seed(42)
    n = 2000

    positive_reviews = [
        "정말 재미있는 영화였어요!", "배우들의 연기가 훌륭했습니다", "감동적인 스토리에 눈물이 났어요",
        "올해 본 영화 중 최고입니다", "두 번 보고 싶은 영화", "가족과 함께 보기 좋은 영화",
        "영상미가 정말 뛰어났습니다", "OST가 너무 좋았어요", "반전이 소름돋았어요",
        "시간 가는 줄 모르고 봤습니다", "강력 추천합니다!", "웃음과 감동이 함께하는 영화"
    ]
    negative_reviews = [
        "시간 낭비였습니다", "스토리가 너무 뻔했어요", "연기가 어색했습니다",
        "돈이 아까운 영화", "지루해서 중간에 나왔어요", "기대했는데 실망스러웠습니다",
        "최악의 영화입니다", "내용이 이해가 안 됩니다", "너무 길고 지루했어요",
        "왜 이걸 만들었는지 모르겠어요", "별로였어요", "다시는 안 볼 영화"
    ]

    labels = np.random.choice([0, 1], n)
    documents = []
    for label in labels:
        if label == 1:
            documents.append(np.random.choice(positive_reviews))
        else:
            documents.append(np.random.choice(negative_reviews))

    df = pd.DataFrame({
        "id": [str(i) for i in range(n)],
        "document": documents,
        "label": labels,
    })

    # 시뮬레이션 예측 결과 (약 90% 정확도)
    correct_mask = np.random.random(n) < 0.90
    df["predicted_label"] = df["label"].copy()
    df.loc[~correct_mask, "predicted_label"] = 1 - df.loc[~correct_mask, "label"]
    df["confidence"] = np.where(correct_mask, np.random.uniform(0.85, 0.99, n), np.random.uniform(0.50, 0.75, n))
    df["is_correct"] = df["label"] == df["predicted_label"]
    df["review_length"] = df["document"].str.len()
    df["length_category"] = pd.cut(df["review_length"], bins=[0, 10, 30, 1000], labels=["짧은", "보통", "긴"])
    df["sentiment_text"] = df["predicted_label"].map({0: "부정", 1: "긍정"})

    return df


# ========== 감성 분석 + 특성 엔지니어링 ==========

def _run_sentiment_analysis(df: pd.DataFrame, model_name: str, progress_bar=None) -> pd.DataFrame:
    """데이터프레임에 감성 분석 결과를 특성 엔지니어링으로 추가합니다."""
    classifier = _load_sentiment_model(model_name)

    # 텍스트 전처리
    texts = df["document"].fillna("").astype(str).tolist()
    texts = [t if t.strip() else "빈 리뷰" for t in texts]

    # 배치 추론
    batch_size = 32
    all_results = []
    total = len(texts)

    for i in range(0, total, batch_size):
        batch = texts[i:i + batch_size]
        results = classifier(batch, batch_size=batch_size)
        all_results.extend(results)
        if progress_bar is not None:
            progress_bar.progress(min((i + batch_size) / total, 1.0))

    # 모델 라벨 매핑 확인 (모델마다 다를 수 있음)
    # WhitePeak 모델: LABEL_0=부정, LABEL_1=긍정 (일반적)
    label_map = {}
    config = classifier.model.config
    if hasattr(config, "id2label"):
        for k, v in config.id2label.items():
            v_lower = v.lower()
            if "neg" in v_lower or v == "LABEL_0":
                label_map[v] = 0
            elif "pos" in v_lower or v == "LABEL_1":
                label_map[v] = 1
            else:
                label_map[v] = int(k)

    # 특성 엔지니어링: 6개 컬럼 추가
    predicted_labels = []
    confidences = []

    for r in all_results:
        pred = label_map.get(r["label"], 0)
        predicted_labels.append(pred)
        confidences.append(r["score"])

    df = df.copy()
    df["predicted_label"] = predicted_labels
    df["confidence"] = confidences
    df["is_correct"] = df["label"] == df["predicted_label"]
    df["review_length"] = df["document"].str.len()
    df["length_category"] = pd.cut(
        df["review_length"],
        bins=[0, 20, 50, 10000],
        labels=["짧은", "보통", "긴"]
    )
    df["sentiment_text"] = df["predicted_label"].map({0: "부정", 1: "긍정"})

    return df


# ========== 메인 로딩 함수 ==========

@st.cache_data(ttl="2h", show_spinner=False)
def _load_movie_data_cached(sample_size: int, model_name: str):
    """캐싱되는 데이터 로딩 함수 (내부용, UI 요소 호출 금지)"""

    # 1순위: 로컬 CSV
    if _LOCAL_CSV.exists():
        try:
            df = _load_local_csv()
            required = ["id", "document", "label", "predicted_label", "confidence"]
            if all(col in df.columns for col in required):
                return df, "local"
        except Exception:
            pass

    # 2순위: HuggingFace datasets 다운로드 → 감성 분석 → 로컬 저장
    try:
        raw_df = _load_raw_nsmc(sample_size)
        df = _run_sentiment_analysis(raw_df, model_name)

        # 로컬에 저장
        _DATA_DIR.mkdir(exist_ok=True)
        df.to_csv(_LOCAL_CSV, index=False, encoding="utf-8-sig")

        return df, "huggingface"
    except Exception:
        pass

    # 3순위: 시뮬레이션 데이터
    df = _generate_simulation_data()
    return df, "simulation"


def load_movie_data(sample_size: int = 2000, model_name: str = DEFAULT_MODEL) -> pd.DataFrame:
    """영화 리뷰 데이터 로딩 — 로컬 → HuggingFace → 시뮬레이션 순서"""
    df, source = _load_movie_data_cached(sample_size, model_name)

    if source == "local":
        st.toast("✅ 로컬 CSV에서 분석 결과를 불러왔습니다.", icon="📂")
    elif source == "huggingface":
        st.toast("✅ NSMC 데이터 다운로드 + 감성 분석 완료!", icon="🌐")
    else:
        st.toast("📊 시뮬레이션 데이터를 사용합니다.", icon="🔄")

    return df


# ========== 유틸리티 함수 ==========

def extract_keywords(texts, top_n=10):
    """간단한 한국어 키워드 추출 (형태소 분석기 불필요)"""
    stopwords = {
        "영화", "정말", "너무", "진짜", "그냥", "이런", "저런", "하는", "있는",
        "없는", "같은", "보는", "하고", "되는", "하지", "않은", "에서", "으로",
        "이다", "있다", "없다", "하다", "되다", "같다", "보다", "나는", "것이",
        "그것", "이것", "저것", "더욱", "매우", "아주", "조금", "많이", "가장"
    }
    words = []
    for t in texts:
        tokens = re.findall(r"[가-힣]{2,}", str(t))
        words.extend([w for w in tokens if w not in stopwords])
    return pd.Series(words).value_counts().head(top_n)
