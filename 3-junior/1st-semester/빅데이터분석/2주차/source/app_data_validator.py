import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="데이터 품질 검증기", page_icon="🧪", layout="wide")

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

st.title("🧪 데이터 전처리 효과 검증기 (Data Validator)")
st.markdown("""
이 도구는 여러분이 수집한 데이터의 **결측치와 이상치가 분석 결과(상관계수)를 얼마나 왜곡하고 있는지** 보여줍니다.
파일을 업로드하고 분석할 두 수치형 컬럼을 선택하세요.
""")

# ──────────────────────────────────────
# 1. 파일 업로드 섹션
# ──────────────────────────────────────
uploaded_file = st.sidebar.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 데이터 로드 (인코딩 고려)
    try:
        df_raw = pd.read_csv(uploaded_file, encoding="utf-8-sig")
    except:
        df_raw = pd.read_csv(uploaded_file, encoding="cp949")

    st.sidebar.success("파일 업로드 완료!")

    # 분석 대상 컬럼 선택 (수치형만 추출)
    numeric_cols = df_raw.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) >= 2:
        col_x = st.sidebar.selectbox("X축 컬럼 (원인)", numeric_cols, index=0)
        col_y = st.sidebar.selectbox("Y축 컬럼 (결과)", numeric_cols, index=1)

        # ──────────────────────────────────────
        # [데이터 전처리 수행]
        # ──────────────────────────────────────
        df_clean = df_raw[[col_x, col_y]].copy()

        # 결측치 처리 (중앙값)
        df_clean[col_x] = df_clean[col_x].fillna(df_clean[col_x].median())
        df_clean[col_y] = df_clean[col_y].fillna(df_clean[col_y].median())

        # 이상치 제거 함수 (IQR)
        def get_outlier_bounds(df, column):
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            return Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

        lower_x, upper_x = get_outlier_bounds(df_clean, col_x)
        lower_y, upper_y = get_outlier_bounds(df_clean, col_y)

        # 이상치가 아닌 데이터만 필터링
        df_final = df_clean[
            (df_clean[col_x] >= lower_x) & (df_clean[col_x] <= upper_x) &
            (df_clean[col_y] >= lower_y) & (df_clean[col_y] <= upper_y)
        ]

        # ──────────────────────────────────────
        # [결과 화면 구성]
        # ──────────────────────────────────────
        row1_col1, row1_col2 = st.columns(2)

        corr_before = df_raw[[col_x, col_y]].corr().iloc[0, 1]
        corr_after = df_final.corr().iloc[0, 1]

        with row1_col1:
            st.metric("전처리 전 상관계수", f"{corr_before:.3f}")
        with row1_col2:
            st.metric("전처리 후 상관계수", f"{corr_after:.3f}",
                      delta=f"{corr_after - corr_before:.3f}",
                      help="이상치 제거 후 변화량")

        st.divider()

        # 시각화
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        sns.scatterplot(data=df_raw, x=col_x, y=col_y,
                        ax=axes[0], color="grey", alpha=0.5)
        axes[0].set_title(f"전처리 전: {col_x} vs {col_y}")

        sns.regplot(data=df_final, x=col_x, y=col_y,
                    ax=axes[1], color="blue", line_kws={"color": "red"})
        axes[1].set_title(f"전처리 후 (이상치 제거 완료)")

        st.pyplot(fig)

        # 데이터 요약 정보
        st.subheader("📋 데이터 정제 요약")
        summary_data = {
            "구분": ["전체 행 수", "결측치 수", "이상치 제거 후 행 수"],
            col_x: [len(df_raw), df_raw[col_x].isnull().sum(), len(df_final)],
            col_y: [len(df_raw), df_raw[col_y].isnull().sum(), len(df_final)]
        }
        st.table(pd.DataFrame(summary_data))

    else:
        st.warning("분석을 위해 최소 2개 이상의 수치형 컬럼이 필요합니다.")
else:
    st.info("왼쪽 사이드바에서 CSV 파일을 업로드하여 분석을 시작하세요.")
    # 샘플 데이터 안내
    if st.button("샘플 데이터로 테스트해보기"):
        st.info("이전 예제 데이터를 활용해 보세요!")
