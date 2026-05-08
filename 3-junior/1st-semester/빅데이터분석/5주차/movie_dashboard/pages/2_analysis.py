# pages/2_analysis.py
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import load_movie_data

st.title("📊 모델 성능 분석")

df = load_movie_data()

if df.empty:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["성능 평가", "신뢰도 분석", "오분류 사례"])

# ═══════ 탭 1: 성능 평가 ═══════
with tab1:
    st.subheader("모델 성능 평가")

    from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

    y_true = df["label"]
    y_pred = df["predicted_label"]

    # KPI 메트릭
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("정확도 (Accuracy)", f"{accuracy_score(y_true, y_pred) * 100:.1f}%")
    m2.metric("정밀도 (Precision)", f"{precision_score(y_true, y_pred) * 100:.1f}%")
    m3.metric("재현율 (Recall)", f"{recall_score(y_true, y_pred) * 100:.1f}%")
    m4.metric("F1-Score", f"{f1_score(y_true, y_pred) * 100:.1f}%")

    st.divider()

    # 혼동행렬
    st.subheader("혼동행렬 (Confusion Matrix)")
    cm = confusion_matrix(y_true, y_pred)
    cm_df = pd.DataFrame(cm, index=["실제 부정", "실제 긍정"], columns=["예측 부정", "예측 긍정"])

    fig = px.imshow(cm_df, text_auto=True, color_continuous_scale="Blues",
                    labels=dict(x="예측", y="실제", color="건수"))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 해석
    tn, fp, fn, tp = cm.ravel()
    st.info(f"""
    **혼동행렬 해석**
    - ✅ 정답 (TN + TP): **{tn + tp:,}건** — 모델이 올바르게 분류한 리뷰
    - ❌ 부정→긍정 오분류 (FP): **{fp:,}건** — 실제 부정인데 긍정으로 잘못 분류
    - ❌ 긍정→부정 오분류 (FN): **{fn:,}건** — 실제 긍정인데 부정으로 잘못 분류
    """)

# ═══════ 탭 2: 신뢰도 분석 ═══════
with tab2:
    st.subheader("신뢰도 분포")

    # 신뢰도 히스토그램
    fig = px.histogram(df, x="confidence", color="is_correct",
                       nbins=30, barmode="overlay", marginal="box",
                       color_discrete_map={True: "#22d3ee", False: "#f87171"},
                       labels={"confidence": "신뢰도", "is_correct": "예측 정답 여부"})
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 정답/오답별 신뢰도 비교
    st.subheader("정답 vs 오답 — 신뢰도 비교")
    col1, col2 = st.columns(2)
    correct = df[df["is_correct"]]
    incorrect = df[~df["is_correct"]]

    with col1:
        st.metric("정답 리뷰 평균 신뢰도", f"{correct['confidence'].mean():.4f}")
        st.metric("정답 리뷰 수", f"{len(correct):,}건")
    with col2:
        st.metric("오답 리뷰 평균 신뢰도", f"{incorrect['confidence'].mean():.4f}" if len(incorrect) > 0 else "N/A")
        st.metric("오답 리뷰 수", f"{len(incorrect):,}건")

    # 신뢰도 구간별 정확도
    st.divider()
    st.subheader("신뢰도 구간별 정확도")
    st.caption("신뢰도가 높을수록 실제 정확도도 높은지 확인합니다.")

    bins = np.arange(0.5, 1.01, 0.05)
    df_temp = df.copy()
    df_temp["conf_bin"] = pd.cut(df_temp["confidence"], bins=bins)
    bin_accuracy = df_temp.groupby("conf_bin", observed=True).agg(
        정확도=("is_correct", "mean"),
        건수=("is_correct", "count")
    ).reset_index()
    bin_accuracy["구간"] = bin_accuracy["conf_bin"].astype(str)
    bin_accuracy["정확도"] = bin_accuracy["정확도"] * 100

    fig = px.bar(bin_accuracy, x="구간", y="정확도",
                 text="건수", color="정확도",
                 color_continuous_scale="Viridis",
                 labels={"정확도": "정확도 (%)", "구간": "신뢰도 구간"})
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 신뢰도가 0.95 이상인 리뷰들의 정확도가 가장 높습니다. 실무에서는 이 임계값을 기준으로 '자동 처리'와 '수동 검토'를 나눌 수 있습니다.")

# ═══════ 탭 3: 오분류 사례 ═══════
with tab3:
    st.subheader("모델이 틀린 리뷰 분석")

    misclassified = df[~df["is_correct"]].copy()

    if len(misclassified) == 0:
        st.success("모든 리뷰를 올바르게 분류했습니다!")
    else:
        # 오분류 유형 필터
        error_type = st.radio(
            "오분류 유형",
            ["전체", "부정→긍정 (FP)", "긍정→부정 (FN)"],
            horizontal=True
        )

        if error_type == "부정→긍정 (FP)":
            misclassified = misclassified[(misclassified["label"] == 0) & (misclassified["predicted_label"] == 1)]
        elif error_type == "긍정→부정 (FN)":
            misclassified = misclassified[(misclassified["label"] == 1) & (misclassified["predicted_label"] == 0)]

        st.write(f"오분류 리뷰: **{len(misclassified):,}건**")

        # 데이터프레임 표시
        display_cols = ["document", "label", "predicted_label", "confidence", "review_length"]
        event = st.dataframe(
            misclassified[display_cols].rename(columns={
                "document": "리뷰 내용",
                "label": "실제 감성",
                "predicted_label": "예측 감성",
                "confidence": "신뢰도",
                "review_length": "글자수"
            }),
            on_select="rerun",
            selection_mode="single-row",
            use_container_width=True,
            height=400,
            column_config={
                "신뢰도": st.column_config.ProgressColumn(min_value=0, max_value=1, format="%.3f"),
                "실제 감성": st.column_config.NumberColumn(format="%d"),
                "예측 감성": st.column_config.NumberColumn(format="%d"),
            }
        )

        # 선택한 리뷰 상세
        selected = event.selection.rows
        if selected:
            row = misclassified.iloc[selected[0]]
            st.divider()
            st.subheader("선택한 리뷰 상세")
            st.markdown(f"> {row['document']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("실제 감성", "긍정" if row["label"] == 1 else "부정")
            c2.metric("모델 예측", "긍정" if row["predicted_label"] == 1 else "부정")
            c3.metric("신뢰도", f"{row['confidence']:.4f}")

        st.info("💡 오분류 사례를 살펴보면, 모호한 표현이나 반어법, 단순 줄거리 나열 등에서 모델이 어려워하는 것을 알 수 있습니다.")
