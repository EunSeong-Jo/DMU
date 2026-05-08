# app.py
import streamlit as st

# 페이지 정의
home = st.Page("../home.py", title="홈", icon="🏠")
chart = st.Page("chart.py", title="차트", icon="📈")
map = st.Page("map.py", title="지도", icon="🌍")
data = st.Page("data.py", title="데이터", icon="📊")

# 네비게이션 설정
pg = st.navigation([home, chart,map, data])
pg.run()