# pages/1_home.py
import streamlit as st
import plotly.express as px
import pandas as pd
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import load_movie_data, extract_keywords

st.title("🎬 영화 리뷰 감성 분석 대시보드")

# ---- 데이터 로딩 ----
df = load_movie_data()

if df.empty:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()

# ---- 사이드바 필터 ----
st.sidebar.subheader("필터")
sentiment_filter = st.sidebar.multiselect(
    "감성", ["긍정", "부정"], default=["긍정", "부정"]
)
confidence_range = st.sidebar.slider(
    "신뢰도 범위", 0.0, 1.0, (0.0, 1.0), step=0.05
)
length_filter = st.sidebar.multiselect(
    "리뷰 길이", ["짧은", "보통", "긴"], default=["짧은", "보통", "긴"]
)

# ---- 필터 적용 ----
filtered = df[
    (df["sentiment_text"].isin(sentiment_filter)) &
    (df["confidence"] >= confidence_range[0]) &
    (df["confidence"] <= confidence_range[1]) &
    (df["length_category"].isin(length_filter))
]

# ---- KPI 카드 ----
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
total = len(filtered)
pos_ratio = (filtered["predicted_label"] == 1).mean() * 100 if total > 0 else 0
accuracy = filtered["is_correct"].mean() * 100 if total > 0 else 0
avg_conf = filtered["confidence"].mean() if total > 0 else 0

kpi1.metric("총 리뷰 수", f"{total:,}건")
kpi2.metric("긍정 비율", f"{pos_ratio:.1f}%", delta=f"{pos_ratio - 50:.1f}%p")
kpi3.metric("모델 정확도", f"{accuracy:.1f}%")
kpi4.metric("평균 신뢰도", f"{avg_conf:.3f}")

st.divider()

# ---- 감성 분포 + 리뷰 길이 분포 ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("감성 분포")
    sentiment_counts = filtered["sentiment_text"].value_counts().reset_index()
    sentiment_counts.columns = ["감성", "건수"]
    fig = px.pie(sentiment_counts, names="감성", values="건수",
                 hole=0.4, color="감성",
                 color_discrete_map={"긍정": "#22d3ee", "부정": "#f87171"})
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("리뷰 길이별 감성 분포")
    fig = px.histogram(filtered, x="review_length", color="sentiment_text",
                       nbins=30, barmode="overlay",
                       color_discrete_map={"긍정": "#22d3ee", "부정": "#f87171"},
                       labels={"review_length": "리뷰 길이 (글자수)", "sentiment_text": "감성"})
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---- 키워드 TOP 10 ----
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("긍정 리뷰 키워드 TOP 10")
    pos_texts = filtered[filtered["predicted_label"] == 1]["document"]
    if len(pos_texts) > 0:
        pos_kw = extract_keywords(pos_texts, top_n=10).reset_index()
        pos_kw.columns = ["키워드", "빈도"]
        fig = px.bar(pos_kw, x="빈도", y="키워드", orientation="h",
                     color_discrete_sequence=["#22d3ee"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"},
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#f8fafc")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("필터 조건에 맞는 긍정 리뷰가 없습니다.")

with col2:
    st.subheader("부정 리뷰 키워드 TOP 10")
    neg_texts = filtered[filtered["predicted_label"] == 0]["document"]
    if len(neg_texts) > 0:
        neg_kw = extract_keywords(neg_texts, top_n=10).reset_index()
        neg_kw.columns = ["키워드", "빈도"]
        fig = px.bar(neg_kw, x="빈도", y="키워드", orientation="h",
                     color_discrete_sequence=["#f87171"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"},
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#f8fafc")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("필터 조건에 맞는 부정 리뷰가 없습니다.")
