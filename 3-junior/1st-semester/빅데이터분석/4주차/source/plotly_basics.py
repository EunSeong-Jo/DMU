# plotly_basics.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Plotly 기초", layout="wide")
st.title('📊 Plotly Express 기본 차트')

# ---- 데이터 생성 ----
np.random.seed(42)
df = pd.DataFrame({
    '월': ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],
    '매출': np.random.randint(500, 3000, 12),
    '이익': np.random.randint(100, 800, 12),
    '고객수': np.random.randint(50, 300, 12),
    '카테고리': np.random.choice(['온라인', '오프라인'], 12)
})

# ---- 탭으로 차트 종류 분류 ----
tab1, tab2, tab3, tab4, tab5 = st.tabs(['선 그래프', '막대 그래프', '산점도', '파이 차트', '히스토그램'])

with tab1:
    st.subheader('Line Chart')
    fig = px.line(df, x='월', y='매출',
                  title='월별 매출 추이',
                  markers=True,
                  color_discrete_sequence=['#22d3ee'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#f8fafc'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader('Bar Chart')
    fig = px.bar(df, x='월', y='매출',
                 color='카테고리',
                 title='월별·채널별 매출',
                 barmode='group',
                 color_discrete_map={'온라인': '#22d3ee', '오프라인': '#a855f7'})
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader('Scatter Plot')
    fig = px.scatter(df, x='고객수', y='매출',
                     size='이익',
                     color='카테고리',
                     hover_name='월',
                     title='고객수 vs 매출 (버블: 이익)')
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader('Pie Chart')
    fig = px.pie(df, names='카테고리', values='매출',
                 title='채널별 매출 비중',
                 color_discrete_map={'온라인': '#22d3ee', '오프라인': '#a855f7'},
                 hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader('Histogram')
    fig = px.histogram(df, x='매출',
                       nbins=8,
                       title='매출 분포',
                       color_discrete_sequence=['#deff9a'])
    st.plotly_chart(fig, use_container_width=True)
