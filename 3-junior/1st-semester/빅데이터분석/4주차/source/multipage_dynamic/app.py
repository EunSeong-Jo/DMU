# app.py
import streamlit as st

st.set_page_config(page_title="동적 네비게이션", page_icon="🔒")

# ---- 역할 상태 관리 ----
if 'role' not in st.session_state:
    st.session_state.role = None

# ---- 역할별 페이지 정의 ----
# 공통 페이지
login_page = st.Page("pages/login.py", title="로그인", icon="🔑")
home_page = st.Page("pages/home.py", title="대시보드", icon="🏠")
data_page = st.Page("pages/data_view.py", title="데이터 조회", icon="📋")

# 관리자 전용 페이지
admin_page = st.Page("pages/admin.py", title="사용자 관리", icon="👥")
settings_page = st.Page("pages/settings.py", title="시스템 설정", icon="⚙️")

# ---- 역할에 따라 메뉴 구성 ----
if st.session_state.role is None:
    # 미로그인: 로그인 페이지만 표시
    pg = st.navigation([login_page])
else:
    # 로그인 후: 역할에 따라 페이지 구성
    page_dict = {
        "분석": [home_page, data_page]
    }

    if st.session_state.role == "admin":
        page_dict["관리"] = [admin_page, settings_page]

    # 로그아웃 페이지 추가
    logout_page = st.Page("pages/logout.py", title="로그아웃", icon="🚪")
    page_dict["계정"] = [logout_page]

    pg = st.navigation(page_dict)

pg.run()
