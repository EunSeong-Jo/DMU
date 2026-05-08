# counter_broken.py
import streamlit as st

st.title('카운터 (실패 버전)')

count = 0

if st.button('클릭! (+1)'):
    count += 1

st.write(f'현재 카운트: {count}')
