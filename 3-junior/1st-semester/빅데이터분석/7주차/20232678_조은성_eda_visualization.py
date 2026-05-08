"""
실습 4: 탐색적 데이터 분석(EDA) + 시각화
========================================
Streamlit + Plotly로 CSIC 2010 HTTP 요청 데이터를 시각적으로 탐색합니다.
정상 요청과 공격 요청의 차이를 직접 눈으로 확인합니다.

실행: streamlit run eda_visualization.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from urllib.parse import unquote
import os
import re

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="CSIC 2010 웹 공격 EDA",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 CSIC 2010 웹 공격 데이터 탐색적 분석")
st.markdown("**HTTP 요청 텍스트에서 공격 패턴을 찾아봅시다!**")


# ============================================================
# 데이터 로드 및 전처리
# ============================================================
@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), "csic2010_requests.csv")
    df = pd.read_csv(data_path)

    # 기본 특성 추출
    df["url_decoded"] = df["url"].apply(
        lambda x: unquote(str(x), encoding="latin-1")
    )
    df["body_decoded"] = df["body"].fillna("").apply(
        lambda x: unquote(str(x), encoding="latin-1")
    )
    df["full_text"] = df["url_decoded"] + " " + df["body_decoded"]
    df["url_length"] = df["url_decoded"].str.len()
    df["body_length"] = df["body_decoded"].str.len()
    df["is_attack"] = (df["label"] == "Anomalous").astype(int)

    return df


df = load_data()

# 사이드바: 기본 정보
st.sidebar.header("📊 데이터 기본 정보")
st.sidebar.metric("전체 HTTP 요청", f"{len(df):,}건")
st.sidebar.metric("정상 (Normal)", f"{(df['label']=='Normal').sum():,}건")
st.sidebar.metric("공격 (Anomalous)", f"{(df['label']=='Anomalous').sum():,}건")
st.sidebar.metric("공격 비율", f"{df['is_attack'].mean()*100:.1f}%")

method_dist = df["method"].value_counts()
st.sidebar.markdown("---")
st.sidebar.subheader("HTTP 메서드")
for method, count in method_dist.items():
    st.sidebar.text(f"  {method}: {count:,}건")


# ============================================================
# 탭 구성
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 분포 분석",
    "📏 길이 분석",
    "🔑 공격 키워드",
    "📄 HTTP 요청 뷰어"
])


# ─── 탭 1: 분포 분석 ──────────────────────────────────────
with tab1:
    st.header("정상 vs 공격 분포")

    col1, col2 = st.columns(2)

    with col1:
        # 정상/공격 파이 차트
        fig = px.pie(
            values=df["label"].value_counts().values,
            names=df["label"].value_counts().index,
            title="정상 vs 공격 비율",
            color_discrete_sequence=["#22d3ee", "#ef4444"],
            hole=0.4
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 메서드별 정상/공격 분포
        cross = pd.crosstab(df["method"], df["label"]).reset_index()
        cross_melted = cross.melt(
            id_vars="method", var_name="label", value_name="count"
        )
        fig = px.bar(
            cross_melted,
            x="method", y="count", color="label",
            title="HTTP 메서드별 정상/공격 분포",
            barmode="group",
            color_discrete_map={"Normal": "#22d3ee", "Anomalous": "#ef4444"}
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    # 메서드별 공격 비율
    st.subheader("메서드별 공격 비율")
    method_attack = df.groupby("method")["is_attack"].agg(["sum", "count"])
    method_attack["attack_ratio"] = method_attack["sum"] / method_attack["count"] * 100
    method_attack.columns = ["공격 건수", "전체 건수", "공격 비율(%)"]
    st.dataframe(method_attack.round(1), use_container_width=True)


# ─── 탭 2: 길이 분석 ──────────────────────────────────────
with tab2:
    st.header("📏 URL / Body 길이 분석")

    col1, col2 = st.columns(2)

    with col1:
        # URL 길이 히스토그램
        fig = px.histogram(
            df,
            x="url_length",
            color="label",
            title="URL 길이 분포 (정상 vs 공격)",
            barmode="overlay",
            opacity=0.7,
            nbins=100,
            color_discrete_map={"Normal": "#22d3ee", "Anomalous": "#ef4444"}
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # URL 길이 Box Plot
        fig = px.box(
            df,
            x="label", y="url_length",
            color="label",
            title="URL 길이 Box Plot",
            color_discrete_map={"Normal": "#22d3ee", "Anomalous": "#ef4444"}
        )
        fig.update_layout(height=450, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # POST 본문 길이 분석
    post_df = df[df["method"] == "POST"].copy()
    if len(post_df) > 0:
        st.subheader("POST 요청 본문(Body) 길이")

        col3, col4 = st.columns(2)
        with col3:
            fig = px.histogram(
                post_df,
                x="body_length",
                color="label",
                title="POST Body 길이 분포",
                barmode="overlay",
                opacity=0.7,
                nbins=80,
                color_discrete_map={"Normal": "#22d3ee", "Anomalous": "#ef4444"}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            fig = px.box(
                post_df,
                x="label", y="body_length",
                color="label",
                title="POST Body 길이 Box Plot",
                color_discrete_map={"Normal": "#22d3ee", "Anomalous": "#ef4444"}
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # 통계 요약
    st.subheader("📊 길이 통계 요약")
    length_stats = df.groupby("label")[["url_length", "body_length"]].agg(
        ["mean", "median", "max"]
    ).round(0)
    st.dataframe(length_stats, use_container_width=True)

    st.info("""
    **관찰**: 공격 요청의 URL이 평균적으로 더 깁니다!
    SQL Injection, XSS 등의 공격 코드가 URL 파라미터에 삽입되면서 길이가 늘어나기 때문입니다.
    """)


# ─── 탭 3: 공격 키워드 분석 ────────────────────────────────
with tab3:
    st.header("🔑 공격 키워드 탐지")
    st.markdown("1교시에서 배운 공격 키워드가 실제 데이터에 얼마나 나타나는지 확인합니다.")

    attack_categories = {
        "SQL Injection": ["'", "select", "union", "drop", "insert",
                          "delete", "update", "or '", "1=1", "--"],
        "XSS": ["<script", "alert(", "onerror", "<iframe",
                "<img", "javascript:", "onfocus"],
        "Path Traversal": ["../", "..\\", "/etc/passwd", "/etc/shadow"],
        "Command Injection": ["; ", "|", "&&", "/bin/", "cat ",
                              "rm ", "wget", "curl"],
        "CRLF Injection": ["%0d", "%0a", "\\r\\n"],
        "Buffer Overflow": [],  # 긴 문자열로 탐지
    }

    # 각 카테고리별 키워드 탐지
    results = []
    for category, keywords in attack_categories.items():
        if not keywords:
            continue
        for kw in keywords:
            normal_count = df[df["label"] == "Normal"]["full_text"].str.contains(
                re.escape(kw), case=False, na=False
            ).sum()
            attack_count = df[df["label"] == "Anomalous"]["full_text"].str.contains(
                re.escape(kw), case=False, na=False
            ).sum()
            results.append({
                "카테고리": category,
                "키워드": kw,
                "정상에서 발견": normal_count,
                "공격에서 발견": attack_count,
                "공격 집중도": attack_count / max(normal_count + attack_count, 1) * 100
            })

    result_df = pd.DataFrame(results)

    # 카테고리별 요약
    col1, col2 = st.columns(2)

    with col1:
        cat_summary = result_df.groupby("카테고리").agg({
            "정상에서 발견": "sum",
            "공격에서 발견": "sum"
        }).reset_index()

        fig = px.bar(
            cat_summary.melt(id_vars="카테고리"),
            x="카테고리", y="value", color="variable",
            title="공격 카테고리별 키워드 출현 빈도",
            barmode="group",
            color_discrete_map={
                "정상에서 발견": "#22d3ee",
                "공격에서 발견": "#ef4444"
            }
        )
        fig.update_layout(height=450, xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 공격 집중도 높은 키워드 Top 15
        top_keywords = result_df.nlargest(15, "공격에서 발견")
        fig = px.bar(
            top_keywords,
            x="키워드", y="공격에서 발견",
            color="카테고리",
            title="공격에서 가장 많이 발견된 키워드 Top 15"
        )
        fig.update_layout(height=450, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # 상세 테이블
    st.subheader("키워드별 상세 현황")
    st.dataframe(
        result_df.sort_values("공격에서 발견", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.success("""
    **핵심 발견**: 1교시에서 배운 공격 키워드가 실제로 공격 요청에 집중적으로 나타납니다!
    이 키워드들을 특성(Feature)으로 추출하면 머신러닝 모델의 학습에 활용할 수 있습니다.
    """)


# ─── 탭 4: HTTP 요청 뷰어 ─────────────────────────────────
with tab4:
    st.header("📄 실제 HTTP 요청 확인")
    st.markdown("정상 요청과 공격 요청의 실제 텍스트를 비교해보세요.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ 정상 요청 (Normal)")
        normal_df = df[df["label"] == "Normal"]
        normal_idx = st.number_input(
            "정상 요청 번호",
            min_value=0,
            max_value=len(normal_df) - 1,
            value=0,
            key="normal_idx"
        )
        normal_row = normal_df.iloc[normal_idx]

        st.text(f"메서드: {normal_row['method']}")
        decoded_url = unquote(str(normal_row["url"]), encoding="latin-1")
        st.text(f"URL (디코딩): {decoded_url}")

        body = str(normal_row["body"]) if pd.notna(normal_row["body"]) and normal_row["body"] else ""
        if body:
            decoded_body = unquote(body, encoding="latin-1")
            st.text(f"Body (디코딩): {decoded_body}")

    with col2:
        st.subheader("🚨 공격 요청 (Anomalous)")
        anomalous_df = df[df["label"] == "Anomalous"]
        anomalous_idx = st.number_input(
            "공격 요청 번호",
            min_value=0,
            max_value=len(anomalous_df) - 1,
            value=0,
            key="anomalous_idx"
        )
        anomalous_row = anomalous_df.iloc[anomalous_idx]

        st.text(f"메서드: {anomalous_row['method']}")
        decoded_url = unquote(str(anomalous_row["url"]), encoding="latin-1")
        st.text(f"URL (디코딩): {decoded_url}")

        body = str(anomalous_row["body"]) if pd.notna(anomalous_row["body"]) and anomalous_row["body"] else ""
        if body:
            decoded_body = unquote(body, encoding="latin-1")
            st.text(f"Body (디코딩): {decoded_body}")

    # 키워드 검색
    st.markdown("---")
    st.subheader("🔍 키워드로 HTTP 요청 검색")

    search_kw = st.text_input(
        "검색할 키워드 (예: SELECT, <script, ../, ' OR)",
        value="select"
    )

    if search_kw:
        full_text = df["url"].fillna("") + " " + df["body"].fillna("")
        matched = df[full_text.str.contains(search_kw, case=False, na=False)]

        st.write(f"**'{search_kw}'** 포함 요청: {len(matched):,}건 "
                 f"(정상: {(matched['label']=='Normal').sum()}, "
                 f"공격: {(matched['label']=='Anomalous').sum()})")

        if len(matched) > 0:
            show_count = min(5, len(matched))
            for i, (_, row) in enumerate(matched.head(show_count).iterrows()):
                label_emoji = "✅" if row["label"] == "Normal" else "🚨"
                decoded_url = unquote(str(row["url"]), encoding="latin-1")
                st.text(f"{label_emoji} [{row['label']}] {row['method']} {decoded_url[:120]}")


# ============================================================
# 하단 요약
# ============================================================
st.markdown("---")
st.header("📝 EDA 핵심 발견")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.success("**발견 1**\n\n공격 URL이 평균적으로 더 길다")
with col2:
    st.success("**발견 2**\n\nSQL/XSS 키워드가 공격에 집중")
with col3:
    st.warning("**발견 3**\n\n개별 공격 유형 라벨은 없음")
with col4:
    st.success("**발견 4**\n\n텍스트에서 공격 패턴 직접 확인 가능!")
