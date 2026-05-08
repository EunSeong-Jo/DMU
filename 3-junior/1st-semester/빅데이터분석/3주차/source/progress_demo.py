# progress_demo.py
import streamlit as st
import time

st.title('진행 표시 바')

if st.button('작업 시작'):
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i + 1)
        time.sleep(0.01)
    st.success('완료!')
