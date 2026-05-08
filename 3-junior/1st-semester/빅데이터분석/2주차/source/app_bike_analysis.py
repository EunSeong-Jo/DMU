import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 한글 폰트 설정
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="서울시 공공자전거 데이터 분석", layout="wide")
st.title("🚴 서울시 공공자전거 이용정보 분석")
st.caption("Part2에서 배운 Pandas 전처리 기법을 활용한 EDA 대시보드")

# ── 데이터 로드 ──
@st.cache_data
def load_data():
    df = pd.read_csv("seoul_bike_10000.csv", encoding="utf-8-sig")
    # 컬럼명 정리 (공백 제거)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ── 사이드바: 필터 ──
st.sidebar.header("🔍 필터")

# 수치형 컬럼 목록
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
category_cols = df.select_dtypes(include=["object"]).columns.tolist()

# ── 탭 구성 ──
tab1, tab2, tab3, tab4 = st.tabs(["📊 데이터 개요", "🔎 이상치 탐지", "📈 시각화", "🧹 전처리 전/후 비교"])

# ═══════════════════════════════════════════
# 탭 1: 데이터 개요
# ═══════════════════════════════════════════
with tab1:
    st.subheader("데이터 미리보기")
    st.dataframe(df.head(20), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 행 수", f"{df.shape[0]:,}")
    with col2:
        st.metric("총 열 수", f"{df.shape[1]}")
    with col3:
        st.metric("결측치 총 수", f"{df.isnull().sum().sum():,}")

    st.subheader("데이터 타입")
    dtype_df = pd.DataFrame({
        "컬럼": df.columns,
        "타입": df.dtypes.values,
        "결측치 수": df.isnull().sum().values,
        "결측치 비율(%)": (df.isnull().sum().values / len(df) * 100).round(2),
        "고유값 수": df.nunique().values
    })
    st.dataframe(dtype_df, use_container_width=True)

    st.subheader("기술통계량")
    st.dataframe(df.describe(), use_container_width=True)

# ═══════════════════════════════════════════
# 탭 2: 이상치 탐지
# ═══════════════════════════════════════════
with tab2:
    st.subheader("IQR 기반 이상치 탐지")
    st.info("IQR = Q3 - Q1, 이상치 기준: Q1 - 1.5×IQR 미만 또는 Q3 + 1.5×IQR 초과")

    selected_col = st.selectbox("분석할 수치형 컬럼 선택", numeric_cols, key="outlier_col")

    if selected_col:
        col_data = df[selected_col].dropna()
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = col_data[(col_data < lower) | (col_data > upper)]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Q1 (25%)", f"{Q1:,.2f}")
        with col2:
            st.metric("Q3 (75%)", f"{Q3:,.2f}")
        with col3:
            st.metric("IQR", f"{IQR:,.2f}")
        with col4:
            st.metric("이상치 수", f"{len(outliers):,}건 ({len(outliers)/len(col_data)*100:.1f}%)")

        st.write(f"**정상 범위:** {lower:,.2f} ~ {upper:,.2f}")

        # 박스플롯
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        axes[0].boxplot(col_data, vert=True)
        axes[0].set_title(f"{selected_col} - 박스플롯")
        axes[0].set_ylabel(selected_col)

        axes[1].hist(col_data, bins=50, color="#22d3ee", edgecolor="white", alpha=0.8)
        axes[1].axvline(lower, color="red", linestyle="--", label=f"하한: {lower:,.0f}")
        axes[1].axvline(upper, color="red", linestyle="--", label=f"상한: {upper:,.0f}")
        axes[1].set_title(f"{selected_col} - 분포")
        axes[1].legend()

        plt.tight_layout()
        st.pyplot(fig)

        # 이상치 데이터 표시
        if len(outliers) > 0:
            st.subheader(f"이상치 데이터 (상위 20건)")
            outlier_df = df[(df[selected_col] < lower) | (df[selected_col] > upper)]
            st.dataframe(outlier_df.head(20), use_container_width=True)

# ═══════════════════════════════════════════
# 탭 3: 시각화
# ═══════════════════════════════════════════
with tab3:
    st.subheader("컬럼별 시각화")

    viz_type = st.radio("차트 유형", ["히스토그램", "산점도", "범주별 집계"], horizontal=True)

    if viz_type == "히스토그램":
        hist_col = st.selectbox("컬럼 선택", numeric_cols, key="hist_col")
        bins = st.slider("구간 수(bins)", 10, 100, 30)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(df[hist_col].dropna(), bins=bins, color="#a855f7", edgecolor="white", alpha=0.8)
        ax.set_title(f"{hist_col} 분포")
        ax.set_xlabel(hist_col)
        ax.set_ylabel("빈도")
        st.pyplot(fig)

    elif viz_type == "산점도":
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X축", numeric_cols, index=0, key="scatter_x")
        with col2:
            y_col = st.selectbox("Y축", numeric_cols, index=min(1, len(numeric_cols)-1), key="scatter_y")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(df[x_col], df[y_col], alpha=0.3, s=10, color="#22d3ee")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{x_col} vs {y_col}")

        # 상관계수 표시
        corr = df[[x_col, y_col]].corr().iloc[0, 1]
        ax.annotate(f"상관계수: {corr:.3f}", xy=(0.02, 0.95), xycoords="axes fraction",
                    fontsize=12, color="red", fontweight="bold")
        st.pyplot(fig)

    elif viz_type == "범주별 집계":
        if category_cols:
            cat_col = st.selectbox("범주 컬럼", category_cols, key="cat_col")
            num_col = st.selectbox("집계 수치 컬럼", numeric_cols, key="agg_col")
            agg_func = st.selectbox("집계 함수", ["합계(sum)", "평균(mean)", "건수(count)"])

            func_map = {"합계(sum)": "sum", "평균(mean)": "mean", "건수(count)": "count"}
            result = df.groupby(cat_col)[num_col].agg(func_map[agg_func]).sort_values(ascending=False).head(20)

            fig, ax = plt.subplots(figsize=(10, 5))
            result.plot(kind="barh", ax=ax, color="#deff9a", edgecolor="white")
            ax.set_title(f"{cat_col}별 {num_col} {agg_func}")
            ax.set_xlabel(num_col)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("범주형 컬럼이 없습니다.")

# ═══════════════════════════════════════════
# 탭 4: 전처리 전/후 비교
# ═══════════════════════════════════════════
with tab4:
    st.subheader("전처리 전/후 비교")
    st.info("IQR 기반으로 이상치를 제거한 전/후를 비교합니다.")

    clean_col = st.selectbox("비교할 컬럼", numeric_cols, key="clean_col")

    if clean_col:
        col_data = df[clean_col].dropna()
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        # 이상치 제거
        cleaned = col_data[(col_data >= lower) & (col_data <= upper)]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 전처리 전")
            st.write(f"- 데이터 수: **{len(col_data):,}**건")
            st.write(f"- 평균: **{col_data.mean():,.2f}**")
            st.write(f"- 중앙값: **{col_data.median():,.2f}**")
            st.write(f"- 표준편차: **{col_data.std():,.2f}**")
            st.write(f"- 최소~최대: {col_data.min():,.2f} ~ {col_data.max():,.2f}")

        with col2:
            st.markdown("#### 전처리 후 (이상치 제거)")
            st.write(f"- 데이터 수: **{len(cleaned):,}**건 ({len(col_data)-len(cleaned)}건 제거)")
            st.write(f"- 평균: **{cleaned.mean():,.2f}**")
            st.write(f"- 중앙값: **{cleaned.median():,.2f}**")
            st.write(f"- 표준편차: **{cleaned.std():,.2f}**")
            st.write(f"- 최소~최대: {cleaned.min():,.2f} ~ {cleaned.max():,.2f}")

        # 전후 비교 차트
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        axes[0].hist(col_data, bins=50, color="#fb7185", edgecolor="white", alpha=0.8)
        axes[0].set_title("전처리 전")
        axes[0].set_xlabel(clean_col)

        axes[1].hist(cleaned, bins=50, color="#22d3ee", edgecolor="white", alpha=0.8)
        axes[1].set_title("전처리 후 (이상치 제거)")
        axes[1].set_xlabel(clean_col)

        plt.tight_layout()
        st.pyplot(fig)

        # 평균 변화
        mean_diff = cleaned.mean() - col_data.mean()
        st.metric("평균 변화량", f"{mean_diff:,.2f}", delta=f"{mean_diff/col_data.mean()*100:.1f}%")
