# pages/2_charts.py
import streamlit as st
import plotly.express as px
import altair as alt
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import load_bike_data

st.title('📊 차트 분석')

df = load_bike_data()

tab1, tab2, tab3 = st.tabs(['월별 패턴', '대여소 비교 (Altair)', '이용시간 분포'])

with tab1:
    st.subheader('월별 대여 패턴')

    # 월별 총 대여건수
    monthly = df.groupby('날짜')['대여건수'].sum().reset_index()
    monthly['월'] = monthly['날짜'].dt.strftime('%Y-%m')

    fig = px.bar(monthly, x='월', y='대여건수',
                 title='월별 총 대여 건수',
                 color='대여건수',
                 color_continuous_scale='YlOrRd')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#f8fafc'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info('💡 봄~여름(4~6월)에 자전거 이용이 급증하는 계절 패턴을 확인할 수 있습니다.')

with tab2:
    st.subheader('대여소별 비교 (Altair 브러시 선택)')

    station_monthly = df.groupby(['날짜', '대여소'])['대여건수'].sum().reset_index()

    # 대여소 TOP 10 기본 선택
    top_stations = df.groupby('대여소')['대여건수'].sum().nlargest(10).index.tolist()
    default_stations = top_stations[:3]

    selected_stations = st.multiselect(
        '비교할 대여소 선택 (2~4개 추천)',
        df['대여소'].unique(),
        default=default_stations,
        key='altair_stations'
    )

    if selected_stations:
        chart_data = station_monthly[station_monthly['대여소'].isin(selected_stations)]

        # 브러시 선택 영역
        brush = alt.selection_interval(encodings=['x'])

        # 상단: 전체 추이 (브러시 영역 선택)
        upper = alt.Chart(chart_data).mark_line(strokeWidth=2, point=True).encode(
            x='날짜:T',
            y='대여건수:Q',
            color='대여소:N',
            tooltip=['날짜:T', '대여소:N', '대여건수:Q']
        ).properties(
            height=250,
            title='날짜 범위를 드래그하여 선택하세요'
        ).add_params(brush)

        # 하단: 선택 범위의 평균 (바 차트)
        lower = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('대여소:N', axis=alt.Axis(labelAngle=0)),
            y='mean(대여건수):Q',
            color='대여소:N',
            tooltip=['대여소:N', 'mean(대여건수):Q']
        ).transform_filter(
            brush
        ).properties(
            height=200,
            title='선택 구간 평균 대여 건수'
        )

        st.altair_chart(upper & lower, use_container_width=True)
    else:
        st.warning('비교할 대여소를 1개 이상 선택하세요.')

with tab3:
    st.subheader('이용 시간 분포')

    fig = px.histogram(df, x='이용시간(분)', nbins=30,
                       title='이용 시간 분포',
                       color_discrete_sequence=['#a855f7'],
                       marginal='box')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#f8fafc'
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric('중앙값', f"{df['이용시간(분)'].median():.0f}분")
    col2.metric('평균', f"{df['이용시간(분)'].mean():.0f}분")
    col3.metric('최댓값', f"{df['이용시간(분)'].max():.0f}분")
