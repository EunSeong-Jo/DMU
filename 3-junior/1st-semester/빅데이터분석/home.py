# Home.py — 멀티페이지 앱 메인 페이지
import streamlit as st

st.set_page_config(page_title="멀티페이지 데모", page_icon="🏠")

st.title('🏠 멀티페이지 앱 데모')

st.write('왼쪽 사이드바에서 페이지를 선택하세요.')

st.markdown("""
### 페이지 목록
- **📈 차트 데모**: 선 차트, 바 차트, 영역 차트
- **🌍 지도 데모**: 서울 주변 지도 시각화
- **📊 데이터 데모**: 인터랙티브 데이터프레임
""")

st.sidebar.success('위에서 페이지를 선택하세요.')