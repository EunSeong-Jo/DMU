# pages/settings.py
import streamlit as st

if st.session_state.get('role') != 'admin':
    st.error('관리자 권한이 필요합니다.')
    st.stop()

st.title('⚙️ 시스템 설정')
st.info('여기는 시스템 설정 페이지입니다.')
