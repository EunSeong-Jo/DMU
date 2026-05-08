# pages/admin.py
import streamlit as st

if st.session_state.get('role') != 'admin':
    st.error('관리자 권한이 필요합니다.')
    st.stop()

st.title('👥 사용자 관리')
st.info('여기는 관리자 전용 페이지입니다.')
