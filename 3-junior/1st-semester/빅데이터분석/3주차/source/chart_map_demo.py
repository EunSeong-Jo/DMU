# chart_map_demo.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('차트와 지도')

# 1. 선 차트
st.subheader('선 차트 (st.line_chart)')
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

# 2. 바 차트
st.subheader('바 차트 (st.bar_chart)')
st.bar_chart(chart_data)

# 3. 지도
st.subheader('지도 (st.map)')
map_data = pd.DataFrame(
    np.random.randn(200, 2) / [50, 50] + [37.5665, 126.9780],  # 서울시청 좌표
    columns=['lat', 'lon']
) # 학교 : [37.5005419, 126.8676709] 
st.map(map_data)
