# 1_📈_차트_데모.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('📈 차트 데모')

df = pd.DataFrame(
    np.random.randn(30, 3),
    columns=['A', 'B', 'C']
)

chart_type = st.radio('차트 종류', ['선 차트', '바 차트', '영역 차트'])

if chart_type == '선 차트':
    st.line_chart(df)
elif chart_type == '바 차트':
    st.bar_chart(df)
else:
    st.area_chart(df)
