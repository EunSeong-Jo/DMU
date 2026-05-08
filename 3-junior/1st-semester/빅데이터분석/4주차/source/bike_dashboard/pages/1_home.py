# pages/1_home.py
import streamlit as st
import plotly.express as px
import pandas as pd
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import load_bike_data, get_station_summary

st.title('🚲 서울시 공공자전거 대시보드')

# ---- 데이터 로딩 (캐싱됨) ----
df = load_bike_data()
summary = get_station_summary(df)

# ---- 사이드바 필터 ----
st.sidebar.subheader('필터')
selected_stations = st.sidebar.multiselect(
    '대여소 선택', df['대여소'].unique(), default=df['대여소'].unique()
)
date_range = st.sidebar.date_input(
    '날짜 범위',
    value=(df['날짜'].min(), df['날짜'].max()),
    min_value=df['날짜'].min(),
    max_value=df['날짜'].max()
)

# ---- 필터 적용 ----
filtered = df[
    (df['대여소'].isin(selected_stations)) &
    (df['날짜'] >= pd.Timestamp(date_range[0])) &
    (df['날짜'] <= pd.Timestamp(date_range[1]))
] if len(date_range) == 2 else df[df['대여소'].isin(selected_stations)]

# ---- KPI 카드 ----
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric('총 대여 건수', f"{filtered['대여건수'].sum():,}건")
kpi2.metric('일 평균 대여', f"{filtered['대여건수'].sum() / max(filtered['날짜'].nunique(), 1):,.0f}건")
kpi3.metric('평균 이용 시간', f"{filtered['이용시간(분)'].mean():.0f}분")
kpi4.metric('대여소 수', f"{filtered['대여소'].nunique()}곳")

st.divider()

# ---- 데이터 기간 표시 ----
st.caption(f"데이터 기간: {filtered['날짜'].min().strftime('%Y.%m')} ~ {filtered['날짜'].max().strftime('%Y.%m')}")

# ---- 월별 추이 차트 (Plotly) ----
monthly = filtered.groupby('날짜')['대여건수'].sum().reset_index()
fig = px.area(monthly, x='날짜', y='대여건수',
              title='월별 대여 건수 추이',
              color_discrete_sequence=['#22d3ee'])
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#f8fafc'
)
st.plotly_chart(fig, use_container_width=True)

# ---- 대여소 TOP 5 ----
col1, col2 = st.columns(2)
with col1:
    st.subheader('대여소별 총 대여 건수 TOP 5')
    top5 = filtered.groupby('대여소')['대여건수'].sum().nlargest(5).reset_index()
    fig = px.bar(top5, x='대여건수', y='대여소', orientation='h',
                 color='대여건수', color_continuous_scale='Viridis')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader('대여소별 매출 비중')
    station_total = filtered.groupby('대여소')['대여건수'].sum().reset_index()
    fig = px.pie(station_total, names='대여소', values='대여건수',
                 hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)
