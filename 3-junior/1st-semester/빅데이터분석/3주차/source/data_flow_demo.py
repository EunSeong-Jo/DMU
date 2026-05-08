# data_flow_demo.py
import streamlit as st
import numpy as np

st.title('Data Flow 체험')

# 버튼을 누를 때마다 스크립트가 재실행되므로 새로운 난수가 생성됨
st.write('랜덤 숫자:', np.random.randn(1))

st.button('다시 실행!')
