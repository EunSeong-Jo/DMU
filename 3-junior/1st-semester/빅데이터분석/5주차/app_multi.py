"""
5주차 실습: 다중 태스크 AI 텍스트 분석 앱 (완성 버전)
실행: streamlit run app_multi.py
"""

import streamlit as st
from transformers import pipeline
import torch

# ─── GPU/CPU 자동 감지 ───
device = 0 if torch.cuda.is_available() else -1

# ─── 페이지 설정 ───
st.set_page_config(
    page_title="AI 텍스트 분석 도구",
    page_icon="🤗",
    layout="wide"
)

# ─── 모델 로드 함수 (캐싱) ───
@st.cache_resource
def load_sentiment_model():
    """감성 분석 모델 로드 (GPU)"""
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=device
    )

@st.cache_resource
def load_zero_shot_model():
    """제로샷 분류 모델 로드 (GPU)"""
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=device
    )

@st.cache_resource
def load_summarizer_model():
    """요약 모델 로드 (GPU)"""
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        device=device
    )

# ─── 사이드바 ───
with st.sidebar:
    st.header("⚙️ 설정")

    task = st.radio(
        "분석 유형을 선택하세요:",
        ["감성 분석", "제로샷 분류", "텍스트 요약"],
        index=0
    )

    st.divider()
    st.markdown("### 📖 모델 정보")

    model_info = {
        "감성 분석": {
            "모델": "DistilBERT (SST-2)",
            "설명": "영어 텍스트의 긍정/부정을 분류합니다.",
            "언어": "영어"
        },
        "제로샷 분류": {
            "모델": "BART-large (MNLI)",
            "설명": "학습 없이 자유로운 카테고리로 분류합니다.",
            "언어": "영어 (다국어 일부 지원)"
        },
        "텍스트 요약": {
            "모델": "DistilBART (CNN)",
            "설명": "긴 텍스트를 짧게 요약합니다.",
            "언어": "영어"
        }
    }

    info = model_info[task]
    st.markdown(f"**모델**: {info['모델']}")
    st.markdown(f"**설명**: {info['설명']}")
    st.markdown(f"**언어**: {info['언어']}")

# ─── 메인 영역 ───
st.title("🤗 AI 텍스트 분석 도구")
st.markdown(f"현재 선택된 분석: **{task}**")

# ─── 감성 분석 ───
if task == "감성 분석":
    st.subheader("😊😞 감성 분석 (Sentiment Analysis)")
    st.markdown("텍스트의 **긍정/부정**을 판별합니다.")

    user_text = st.text_area(
        "분석할 텍스트를 입력하세요:",
        placeholder="예: I love learning new things!",
        height=120,
        key="sentiment_input"
    )

    # 예시 문장 제공
    st.markdown("**예시 문장** (클릭하여 복사)")
    col1, col2 = st.columns(2)
    with col1:
        st.code("I love this product! It works great.", language=None)
        st.code("The weather is beautiful today.", language=None)
    with col2:
        st.code("This is the worst experience ever.", language=None)
        st.code("I'm very disappointed with the service.", language=None)

    if st.button("분석하기 🔍", type="primary", key="sentiment_btn"):
        if user_text.strip():
            with st.spinner("모델 로딩 및 분석 중..."):
                classifier = load_sentiment_model()
                result = classifier(user_text)

            label = result[0]['label']
            score = result[0]['score']

            st.divider()

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                if label == "POSITIVE":
                    st.success(f"### 😊 긍정 (POSITIVE)")
                else:
                    st.error(f"### 😞 부정 (NEGATIVE)")

            with col2:
                st.metric("확신도", f"{score:.1%}")

            with col3:
                st.metric("라벨", label)

            # 확신도 시각화
            st.progress(score)

            # 결과 상세
            with st.expander("상세 결과 보기"):
                st.json(result[0])
        else:
            st.warning("텍스트를 입력해주세요!")

# ─── 제로샷 분류 ───
elif task == "제로샷 분류":
    st.subheader("🏷️ 제로샷 분류 (Zero-Shot Classification)")
    st.markdown("**학습 없이** 자유롭게 카테고리를 지정하여 분류합니다.")

    user_text = st.text_area(
        "분류할 텍스트를 입력하세요:",
        placeholder="예: Apple announced a new MacBook with M4 chip.",
        height=120,
        key="zero_shot_input"
    )

    categories = st.text_input(
        "분류 카테고리 (쉼표로 구분):",
        value="technology, sports, politics, entertainment, science",
        key="categories_input"
    )

    if st.button("분류하기 🏷️", type="primary", key="zero_shot_btn"):
        if user_text.strip() and categories.strip():
            labels = [c.strip() for c in categories.split(",")]

            with st.spinner("모델 로딩 및 분류 중..."):
                zero_clf = load_zero_shot_model()
                result = zero_clf(user_text, candidate_labels=labels)

            st.divider()
            st.subheader("분류 결과")

            # 결과를 바 차트로 표시
            import pandas as pd

            df = pd.DataFrame({
                "카테고리": result['labels'],
                "확률": result['scores']
            })

            st.bar_chart(df.set_index("카테고리"))

            # 최상위 결과 강조
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            st.success(f"**최상위 분류: {top_label}** (확률: {top_score:.1%})")

            # 전체 결과 테이블
            with st.expander("전체 결과 보기"):
                df['확률(%)'] = df['확률'].apply(lambda x: f"{x:.2%}")
                st.dataframe(df, use_container_width=True)
        else:
            st.warning("텍스트와 카테고리를 모두 입력해주세요!")

# ─── 텍스트 요약 ───
elif task == "텍스트 요약":
    st.subheader("📝 텍스트 요약 (Summarization)")
    st.markdown("긴 텍스트를 **짧게 요약**합니다.")

    user_text = st.text_area(
        "요약할 텍스트를 입력하세요:",
        placeholder="긴 영어 텍스트를 입력하세요 (최소 50단어 이상 권장)...",
        height=200,
        key="summary_input"
    )

    # 요약 길이 설정
    col1, col2 = st.columns(2)
    with col1:
        max_len = st.slider("최대 요약 길이 (토큰)", 30, 150, 60, key="max_len")
    with col2:
        min_len = st.slider("최소 요약 길이 (토큰)", 10, 50, 20, key="min_len")

    # 예시 텍스트 제공
    with st.expander("예시 텍스트 보기"):
        sample_text = """Artificial intelligence has transformed many industries in recent years. From healthcare to finance, AI systems are being deployed to automate tasks that previously required human intelligence. Machine learning, a subset of AI, has been particularly impactful, enabling computers to learn from data without being explicitly programmed. Deep learning, which uses neural networks with many layers, has achieved remarkable results in image recognition, natural language processing, and game playing. However, concerns about AI safety, bias, and job displacement continue to be important topics of discussion in both academic and public spheres."""
        st.text(sample_text)
        if st.button("이 텍스트 사용하기"):
            st.session_state["summary_input"] = sample_text
            st.rerun()

    if st.button("요약하기 📝", type="primary", key="summary_btn"):
        if user_text.strip():
            word_count = len(user_text.split())

            if word_count < 30:
                st.warning("요약하기에 텍스트가 너무 짧습니다. 최소 30단어 이상 입력해주세요.")
            else:
                with st.spinner("모델 로딩 및 요약 중..."):
                    summarizer = load_summarizer_model()
                    result = summarizer(
                        user_text,
                        max_length=max_len,
                        min_length=min_len
                    )

                st.divider()
                st.subheader("요약 결과")

                # 원문/요약 비교
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**📄 원문**")
                    st.info(user_text)
                    st.caption(f"단어 수: {word_count}")

                with col2:
                    summary_text = result[0]['summary_text']
                    summary_word_count = len(summary_text.split())
                    st.markdown("**📋 요약**")
                    st.success(summary_text)
                    st.caption(f"단어 수: {summary_word_count}")

                # 압축률 표시
                ratio = (1 - summary_word_count / word_count) * 100
                st.metric("압축률", f"{ratio:.0f}%",
                         delta=f"{word_count - summary_word_count}단어 감소")
        else:
            st.warning("텍스트를 입력해주세요!")

# ─── 푸터 ───
st.divider()
st.caption("🤗 Powered by HuggingFace Transformers | 5주차 실습")
