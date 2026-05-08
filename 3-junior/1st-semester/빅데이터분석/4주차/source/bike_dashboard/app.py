# app.py
import streamlit as st

st.set_page_config(
    page_title="따릉이 대시보드",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 페이지 정의
home = st.Page("pages/1_home.py", title="대시보드", icon="🏠", default=True)
charts = st.Page("pages/2_charts.py", title="차트 분석", icon="📊")
data = st.Page("pages/3_data.py", title="데이터 조회", icon="🔍")

pg = st.navigation({
    "따릉이 분석": [home, charts, data]
})

# 사이드바 공통 요소
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Seoul_Bike_logo.svg/200px-Seoul_Bike_logo.svg.png", width=100)
st.sidebar.markdown("---")
st.sidebar.caption("4주차 실습 프로젝트")

pg.run()
