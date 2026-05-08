# altair_basics.py
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(page_title="Altair 기초", layout="wide")
st.title('📈 Altair 기본 차트')

# ---- 데이터 ----
np.random.seed(42)
dates = pd.date_range('2025-01-01', periods=90)
df = pd.DataFrame({
    '날짜': dates,
    '매출': np.cumsum(np.random.randn(90) * 50 + 10),
    '카테고리': np.tile(['A', 'B', 'C'], 30)
})

tab1, tab2, tab3 = st.tabs(['선 그래프', '막대 그래프', '산점도 + 인터랙션'])

with tab1:
    st.subheader('Line Chart')
    chart = alt.Chart(df).mark_line(strokeWidth=2).encode(
        x='날짜:T',              # T = Temporal (시간)
        y='매출:Q',              # Q = Quantitative (수치)
        color='카테고리:N',      # N = Nominal (명목형)
        tooltip=['날짜:T', '매출:Q', '카테고리:N']
    ).properties(
        height=400
    ).interactive()              # 줌/팬 활성화

    st.altair_chart(chart, use_container_width=True)

with tab2:
    st.subheader('Bar Chart')
    bar_data = df.groupby('카테고리')['매출'].mean().reset_index()
    chart = alt.Chart(bar_data).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X('카테고리:N', axis=alt.Axis(labelAngle=0)),
        y='매출:Q',
        color=alt.Color('카테고리:N', legend=None),
        tooltip=['카테고리', '매출']
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

with tab3:
    st.subheader('Scatter + 브러시 선택')

    # 브러시 선택 영역 정의
    brush = alt.selection_interval()

    scatter = alt.Chart(df).mark_circle(size=60).encode(
        x='날짜:T',
        y='매출:Q',
        color=alt.condition(brush, '카테고리:N', alt.value('lightgray')),
        tooltip=['날짜:T', '매출:Q', '카테고리:N']
    ).add_params(brush).properties(height=400)

    st.altair_chart(scatter, use_container_width=True)
    st.caption('드래그로 영역을 선택하면 해당 점만 색상이 표시됩니다')
