# counter_fixed.py
import streamlit as st

st.title('카운터 (성공 버전)')

# session_state: 재실행되어도 값이 유지되는 특별한 저장소
if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button('클릭! (+1)'):
    st.session_state.count += 1

st.write(f'현재 카운트: {st.session_state.count}')
