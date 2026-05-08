# columns_demo.py
import streamlit as st
import numpy as np
import pandas as pd

st.title('컬럼 레이아웃')

# ---- 1:1 균등 분할 ----
st.subheader('1:1 배치')
col1, col2 = st.columns(2)

with col1:
    st.write('왼쪽 컬럼')
    st.line_chart(np.random.randn(20, 1))

with col2:
    st.write('오른쪽 컬럼')
    st.bar_chart(np.random.randn(20, 1))

# ---- 2:1 비율 분할 ----
st.subheader('2:1 배치 (메인 차트 강조)')
main_col, side_col = st.columns([2, 1])

with main_col:
    st.write('메인 차트 (넓은 영역)')
    chart_data = pd.DataFrame(np.random.randn(30, 3), columns=['A', 'B', 'C'])
    st.line_chart(chart_data)

with side_col:
    st.write('요약 정보')
    st.metric("평균 A", f"{chart_data['A'].mean():.2f}")
    st.metric("평균 B", f"{chart_data['B'].mean():.2f}")
    st.metric("평균 C", f"{chart_data['C'].mean():.2f}")
