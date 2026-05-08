import streamlit as st
import plotly.express as px      # 1) 라이브러리 가져오기
import pandas as pd

df = pd.DataFrame({
    '월': ['1월', '2월', '3월', '4월', '5월', '6월'],
    '매출': [100, 150, 130, 180, 200, 170]
})

fig = px.line(df, x='월', y='매출')  # 2) 차트 생성 → fig 객체 반환
#     ↑                               fig = Figure (차트 객체)
#     px.차트종류(데이터, x축, y축)

fig.update_layout(title='제목')   # 3) 스타일 수정 (선택사항)

st.plotly_chart(fig)              # 4) Streamlit에 표시