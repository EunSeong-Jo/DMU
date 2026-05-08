# pages/login.py
import streamlit as st

st.title('🔑 로그인')

# 간단한 시뮬레이션 (실제로는 DB 인증)
USERS = {
    'admin': {'password': '1234', 'role': 'admin'},
    'user': {'password': '1234', 'role': 'viewer'}
}

with st.form('login_form'):
    username = st.text_input('사용자 이름')
    password = st.text_input('비밀번호', type='password')
    submitted = st.form_submit_button('로그인')

if submitted:
    if username in USERS and USERS[username]['password'] == password:
        st.session_state.role = USERS[username]['role']
        st.session_state.username = username
        st.success(f'{username}님, 환영합니다! ({USERS[username]["role"]})')
        st.rerun()
    else:
        st.error('사용자 이름 또는 비밀번호가 올바르지 않습니다.')
