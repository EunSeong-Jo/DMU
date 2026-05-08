# form_demo.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Form 데모", layout="wide")
st.title('📋 st.form() — 입력을 모아서 제출')

# ---- 데이터 준비 ----
np.random.seed(42)
df = pd.DataFrame({
    '이름': [f'학생{i}' for i in range(1, 51)],
    '학과': np.random.choice(['컴퓨터공학', 'AI소프트웨어', '정보보안', '데이터사이언스'], 50),
    '학년': np.random.choice([1, 2, 3, 4], 50),
    '점수': np.random.randint(40, 100, 50)
})

# ---- Form: 필터를 모아서 한 번에 적용 ----
with st.form('filter_form'):
    st.subheader('🔍 필터 설정')

    col1, col2, col3 = st.columns(3)
    with col1:
        dept = st.selectbox('학과', ['전체'] + list(df['학과'].unique()))
    with col2:
        grade = st.selectbox('학년', ['전체', 1, 2, 3, 4])
    with col3:
        min_score = st.slider('최소 점수', 0, 100, 60)

    # 제출 버튼 — 이 버튼을 눌러야 필터가 적용됨
    submitted = st.form_submit_button('🔎 필터 적용', use_container_width=True)

# ---- 필터 적용 ----
filtered = df.copy()
if submitted or True:  # 항상 현재 필터 상태로 표시
    if dept != '전체':
        filtered = filtered[filtered['학과'] == dept]
    if grade != '전체':
        filtered = filtered[filtered['학년'] == grade]
    filtered = filtered[filtered['점수'] >= min_score]

# ---- 결과 표시 ----
st.subheader(f'검색 결과: {len(filtered)}명')

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric('인원수', f'{len(filtered)}명')
kpi2.metric('평균 점수', f'{filtered["점수"].mean():.1f}점' if len(filtered) > 0 else '-')
kpi3.metric('최고 점수', f'{filtered["점수"].max()}점' if len(filtered) > 0 else '-')

st.dataframe(filtered, use_container_width=True)
