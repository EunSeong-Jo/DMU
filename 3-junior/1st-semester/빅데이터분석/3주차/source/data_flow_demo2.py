# data_flow_demo2.py
import streamlit as st
import numpy as np
from datetime import datetime

st.title('재실행 확인')

# 실행 시각을 출력하여 재실행을 눈으로 확인
st.write('현재 시각:', datetime.now().strftime('%H:%M:%S'))

name = st.text_input('이름을 입력하세요')
st.write(f'안녕하세요, {name}님!')

number = st.slider('숫자를 선택하세요', 0, 100, 50)
st.write(f'선택한 숫자: {number}')
