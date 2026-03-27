# 3_📊_데이터_데모.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('📊 데이터 데모')

np.random.seed(42)
df = pd.DataFrame(
    np.random.randn(50, 5),
    columns=['매출', '비용', '이익', '고객수', '만족도']
)

# 다중 선택으로 컬럼 필터
columns = st.multiselect('표시할 컬럼', df.columns.tolist(), default=['매출', '이익'])

if columns:
    st.dataframe(df[columns], use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('기술통계')
        st.dataframe(df[columns].describe())
    with col2:
        st.subheader('차트')
        st.line_chart(df[columns])
else:
    st.warning('컬럼을 하나 이상 선택하세요.')
