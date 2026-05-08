# altair_layered.py
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(page_title="Altair 레이어드", layout="wide")
st.title('📊 Altair 레이어드 차트 — 주석 달기')

# ---- 주가 데이터 시뮬레이션 ----
np.random.seed(42)
dates = pd.date_range('2025-01-01', periods=180, freq='D')
prices = 50000 + np.cumsum(np.random.randn(180) * 500)
df = pd.DataFrame({'날짜': dates, '주가': prices})

# ---- 주석(annotation) 데이터 ----
annotations = pd.DataFrame({
    '날짜': pd.to_datetime(['2025-02-14', '2025-04-01', '2025-06-15']),
    '주가': [df.loc[df['날짜'] == '2025-02-14', '주가'].values[0],
             df.loc[df['날짜'] == '2025-04-01', '주가'].values[0],
             df.loc[df['날짜'] == '2025-06-15', '주가'].values[0]],
    '마커': ['⚡', '📈', '🔥'],
    '설명': ['실적 발표', '신제품 출시', '최고가 경신']
})

# ---- Layer 1: 선 그래프 (주가 추이) ----
line = alt.Chart(df).mark_line(color='#22d3ee', strokeWidth=2).encode(
    x='날짜:T',
    y=alt.Y('주가:Q', scale=alt.Scale(zero=False)),
    tooltip=['날짜:T', '주가:Q']
)

# ---- Layer 2: 호버 포인트 ----
nearest = alt.selection_point(nearest=True, on='pointerover', fields=['날짜'], empty=False)

points = alt.Chart(df).mark_point(size=80, color='#22d3ee').encode(
    x='날짜:T',
    y='주가:Q',
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
).add_params(nearest)

# ---- Layer 3: 수직 룰 (호버 가이드라인) ----
rules = alt.Chart(df).mark_rule(color='gray', strokeDash=[4,4]).encode(
    x='날짜:T',
    opacity=alt.condition(nearest, alt.value(0.5), alt.value(0))
).add_params(nearest)

# ---- Layer 4: 주석 마커 ----
annotation_marks = alt.Chart(annotations).mark_text(
    size=24, dy=-20
).encode(
    x='날짜:T',
    y='주가:Q',
    text='마커:N',
    tooltip=['설명:N', '날짜:T', '주가:Q']
)

# ---- 모든 레이어 합성 ----
chart = (line + points + rules + annotation_marks).properties(
    height=450,
    title='시뮬레이션 주가 차트 (주석 포함)'
).interactive()

st.altair_chart(chart, use_container_width=True)
st.caption('마우스를 올리면 포인트와 가이드라인이 표시됩니다. 이모지 마커를 호버하면 이벤트 설명이 나타납니다.')
