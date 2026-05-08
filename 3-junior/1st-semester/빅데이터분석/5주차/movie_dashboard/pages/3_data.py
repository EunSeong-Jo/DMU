# pages/3_data.py
import streamlit as st
import pandas as pd
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import load_movie_data

st.title("🔍 데이터 조회")

df = load_movie_data()

if df.empty:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()

tab1, tab2 = st.tabs(["특성 엔지니어링 결과", "원본 데이터"])

# ═══════ 탭 1: 특성 엔지니어링 결과 ═══════
with tab1:
    st.subheader("특성 엔지니어링 결과")
    st.caption("원본 3개 컬럼(id, document, label)에 모델 분석 결과 6개 컬럼이 추가되었습니다.")

    # 필터
    with st.form("fe_filter"):
        col1, col2, col3 = st.columns(3)
        with col1:
            sentiment_filter = st.multiselect(
                "감성", ["긍정", "부정"], default=["긍정", "부정"], key="fe_sentiment"
            )
        with col2:
            correct_filter = st.multiselect(
                "예측 결과", ["정답", "오답"], default=["정답", "오답"], key="fe_correct"
            )
        with col3:
            conf_range = st.slider("신뢰도 범위", 0.0, 1.0, (0.0, 1.0), key="fe_conf")
        submitted = st.form_submit_button("필터 적용", use_container_width=True)

    # 필터 적용
    correct_map = {"정답": True, "오답": False}
    filtered = df[
        (df["sentiment_text"].isin(sentiment_filter)) &
        (df["is_correct"].isin([correct_map[c] for c in correct_filter])) &
        (df["confidence"] >= conf_range[0]) &
        (df["confidence"] <= conf_range[1])
    ]

    st.write(f"검색 결과: **{len(filtered):,}건** / 전체 {len(df):,}건")

    # 데이터프레임 표시
    event = st.dataframe(
        filtered,
        on_select="rerun",
        selection_mode="multi-row",
        use_container_width=True,
        height=400,
        column_config={
            "confidence": st.column_config.ProgressColumn(
                "신뢰도", min_value=0, max_value=1, format="%.3f"
            ),
            "is_correct": st.column_config.CheckboxColumn("정답 여부"),
            "review_length": st.column_config.NumberColumn("리뷰 길이", format="%d자"),
            "label": st.column_config.NumberColumn("실제 감성", format="%d"),
            "predicted_label": st.column_config.NumberColumn("예측 감성", format="%d"),
        }
    )

    # 선택한 리뷰 상세
    selected = event.selection.rows
    if selected:
        st.divider()
        selected_rows = filtered.iloc[selected]
        st.subheader(f"선택한 리뷰 ({len(selected)}건)")

        for _, row in selected_rows.iterrows():
            actual = "긍정" if row["label"] == 1 else "부정"
            pred = "긍정" if row["predicted_label"] == 1 else "부정"
            icon = "✅" if row["is_correct"] else "❌"
            st.markdown(f"""
            {icon} **실제**: {actual} | **예측**: {pred} | **신뢰도**: {row['confidence']:.4f}
            > {row['document']}
            """)

    st.divider()

    # CSV 다운로드
    csv = filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 특성 엔지니어링 결과 CSV 다운로드",
        data=csv,
        file_name="nsmc_feature_engineered.csv",
        mime="text/csv"
    )

    # 특성 엔지니어링 설명
    with st.expander("💡 특성 엔지니어링이란?"):
        st.markdown("""
        **특성 엔지니어링(Feature Engineering)** 은 원본 데이터에 새로운 특성(컬럼)을 추가하여
        데이터의 분석 가치를 높이는 과정입니다.

        | 원본 컬럼 | 추가된 컬럼 | 생성 방법 |
        |-----------|-------------|-----------|
        | `id` | `predicted_label` | HuggingFace 모델의 예측 결과 (0/1) |
        | `document` | `confidence` | 모델의 예측 신뢰도 (0~1) |
        | `label` | `is_correct` | 실제 label과 예측의 일치 여부 |
        | | `review_length` | 리뷰 텍스트의 글자 수 |
        | | `length_category` | 길이 범주 (짧은/보통/긴) |
        | | `sentiment_text` | 예측 감성의 텍스트 표현 |

        원본 **3개 컬럼 → 9개 컬럼**으로 확장되어, 모델 성능 평가와 다양한 분석이 가능해집니다.
        """)

# ═══════ 탭 2: 원본 데이터 ═══════
with tab2:
    st.subheader("원본 NSMC 데이터")

    # 컬럼 선택
    all_columns = df.columns.tolist()
    original_cols = ["id", "document", "label"]
    selected_columns = st.multiselect(
        "표시할 컬럼 선택", all_columns, default=original_cols, key="raw_cols"
    )

    if not selected_columns:
        st.warning("컬럼을 1개 이상 선택하세요.")
    else:
        # 텍스트 검색
        with st.form("raw_filter"):
            col1, col2 = st.columns(2)
            with col1:
                search_text = st.text_input("리뷰 내용 검색", placeholder="검색어 입력...")
            with col2:
                label_filter = st.multiselect(
                    "실제 감성 (label)", [0, 1], default=[0, 1],
                    format_func=lambda x: "긍정 (1)" if x == 1 else "부정 (0)"
                )
            submitted = st.form_submit_button("검색", use_container_width=True)

        raw_filtered = df[df["label"].isin(label_filter)]
        if search_text:
            raw_filtered = raw_filtered[
                raw_filtered["document"].str.contains(search_text, case=False, na=False)
            ]

        st.write(f"검색 결과: **{len(raw_filtered):,}건** / 전체 {len(df):,}건 | 컬럼: {len(selected_columns)}개")
        st.dataframe(raw_filtered[selected_columns], use_container_width=True, height=400)

        # CSV 다운로드
        csv = raw_filtered[selected_columns].to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 원본 데이터 CSV 다운로드",
            data=csv,
            file_name="nsmc_raw.csv",
            mime="text/csv",
            key="raw_download"
        )
