# app.py
import streamlit as st

st.set_page_config(
    page_title="영화 리뷰 감성 분석",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 페이지 정의
home = st.Page("pages/1_home.py", title="대시보드", icon="🏠", default=True)
analysis = st.Page("pages/2_analysis.py", title="모델 성능 분석", icon="📊")
data = st.Page("pages/3_data.py", title="데이터 조회", icon="🔍")

pg = st.navigation({
    "영화 리뷰 분석": [home, analysis, data]
})

# 사이드바 공통 요소
st.sidebar.markdown("### 🎬 NSMC 영화 리뷰")
st.sidebar.caption("네이버 영화 리뷰 감성 분석 대시보드")
st.sidebar.markdown("---")
st.sidebar.caption("5주차 실습 프로젝트")

pg.run()
