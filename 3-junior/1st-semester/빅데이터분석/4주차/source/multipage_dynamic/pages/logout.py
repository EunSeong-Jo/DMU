# pages/logout.py
import streamlit as st

st.title('🚪 로그아웃')

if st.button('로그아웃'):
    st.session_state.role = None
    st.session_state.username = None
    st.rerun()
