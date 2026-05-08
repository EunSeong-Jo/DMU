# pages/home.py
import streamlit as st

st.title('🏠 대시보드')
st.write(f'환영합니다, **{st.session_state.get("username", "")}**님!')
st.info('여기는 대시보드 페이지입니다.')
