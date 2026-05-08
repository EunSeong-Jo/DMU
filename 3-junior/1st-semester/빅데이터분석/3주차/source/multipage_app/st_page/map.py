# 2_🌍_지도_데모.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('🌍 지도 데모')

center = st.selectbox('중심 위치', ['서울시청', '동양미래대학교'])

coords = {
    '서울시청': [37.5665, 126.9780],
    '동양미래대학교': [37.5005419, 126.8676709],
}

lat, lon = coords[center]

map_data = pd.DataFrame(
    np.random.randn(200, 2) / [50, 50] + [lat, lon],
    columns=['lat', 'lon']
)

st.map(map_data)
st.caption(f'중심 좌표: {lat}, {lon}')
