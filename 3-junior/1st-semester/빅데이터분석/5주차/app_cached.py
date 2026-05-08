"""
5주차 실습: 감성 분석 웹 앱 (캐싱 적용 버전)
실행: streamlit run app_cached.py
"""

import streamlit as st
from transformers import pipeline
import torch

# ─── GPU/CPU 자동 감지 ───
device = 0 if torch.cuda.is_available() else -1

# ─── 페이지 설정 ───
st.set_page_config(
    page_title="AI 감성 분석기",
    page_icon="🤗",
    layout="centered"
)

# ─── 모델 로드 (캐싱!) ───
@st.cache_resource
def load_model():
    """모델을 로드하고 캐싱합니다. 최초 1회만 실행됩니다."""
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=device
    )

classifier = load_model()  # 캐시된 모델 사용

# ─── 제목 ───
st.title("🤗 AI 감성 분석기")
st.markdown("텍스트를 입력하면 **긍정/부정**을 분석합니다.")
st.caption("✅ 모델이 캐싱되어 빠르게 동작합니다!")

# ─── 사용자 입력 ───
user_text = st.text_area(
    "분석할 텍스트를 입력하세요:",
    placeholder="예: I love this course!",
    height=100
)

# ─── 분석 버튼 ───
if st.button("분석하기 🔍", type="primary"):
    if user_text.strip():
        with st.spinner("AI가 분석 중입니다..."):
            result = classifier(user_text)

        label = result[0]['label']
        score = result[0]['score']

        # 결과 표시
        st.divider()
        st.subheader("분석 결과")

        col1, col2 = st.columns(2)

        with col1:
            if label == "POSITIVE":
                st.success(f"😊 **긍정** (POSITIVE)")
            else:
                st.error(f"😞 **부정** (NEGATIVE)")

        with col2:
            st.metric("확신도", f"{score:.1%}")

        st.progress(score)
    else:
        st.warning("텍스트를 입력해주세요!")
