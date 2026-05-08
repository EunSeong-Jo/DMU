"""
5주차 실습: 감성 분석 웹 앱 (기본 버전)
실행: streamlit run app_basic.py
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

# ─── 제목 ───
st.title("🤗 AI 감성 분석기")
st.markdown("텍스트를 입력하면 **긍정/부정**을 분석합니다.")

# ─── 모델 로드 ───
# ⚠️ 모델 파일 다운로드는 HuggingFace 로컬 캐시(~/.cache/huggingface/hub/)에 저장되어 1회만 발생.
# 하지만 디스크→RAM→GPU 로드는 pipeline() 호출마다 매번 반복됨! → Step 2에서 해결
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=device
)

# ─── 사용자 입력 ───
user_text = st.text_area(
    "분석할 텍스트를 입력하세요:",
    placeholder="예: I love this course!",
    height=100
)

# ─── 분석 버튼 ───
if st.button("분석하기 🔍", type="primary"):
    if user_text.strip():
        # 분석 실행
        with st.spinner("AI가 분석 중입니다..."):
            result = classifier(user_text)

        label = result[0]['label']
        score = result[0]['score']

        # 결과 표시
        st.divider()
        st.subheader("분석 결과")

        if label == "POSITIVE":
            st.success(f"😊 **긍정** (POSITIVE)")
        else:
            st.error(f"😞 **부정** (NEGATIVE)")

        # 확신도 표시
        st.metric("확신도", f"{score:.1%}")
        st.progress(score)
    else:
        st.warning("텍스트를 입력해주세요!")
