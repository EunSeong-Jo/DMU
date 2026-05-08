# dataframe_selection.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="행 선택", layout="wide")
st.title('🔍 데이터프레임 행 선택 → 차트 비교')

# ---- 데이터 ----
np.random.seed(42)
products = ['노트북', '태블릿', '스마트폰', '이어폰', '스마트워치', '키보드', '마우스', '모니터']
df = pd.DataFrame({
    '제품': products,
    '매출(억)': np.random.randint(10, 200, len(products)),
    '성장률(%)': np.random.uniform(-5, 25, len(products)).round(1),
    '월별추이': [np.random.randint(5, 30, 12).tolist() for _ in products]
})

st.subheader('제품 목록 (행을 클릭하여 선택)')

# ---- 행 선택 가능한 데이터프레임 ----
event = st.dataframe(
    df[['제품', '매출(억)', '성장률(%)']],
    on_select="rerun",
    selection_mode="multi-row",
    use_container_width=True,
    column_config={
        '성장률(%)': st.column_config.ProgressColumn(
            min_value=-10, max_value=30, format='%.1f%%'
        )
    }
)

# ---- 선택된 행으로 비교 차트 ----
selected_rows = event.selection.rows
if selected_rows:
    selected_df = df.iloc[selected_rows]
    st.subheader(f'선택한 {len(selected_rows)}개 제품 비교')

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(selected_df, x='제품', y='매출(억)',
                     color='제품', title='매출 비교')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(selected_df, x='제품', y='성장률(%)',
                     color='제품', title='성장률 비교')
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info('💡 위 테이블에서 행을 클릭하면 비교 차트가 표시됩니다.')
