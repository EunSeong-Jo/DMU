# interactive_explorer.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('인터랙티브 데이터 탐색기')

# ---- 데이터 생성 ----
np.random.seed(42)
df = pd.DataFrame({
    '날짜': pd.date_range('2026-01-01', periods=100),
    '매출': np.random.randint(50, 500, 100),
    '방문자': np.random.randint(100, 1000, 100),
    '전환율': np.random.uniform(0.01, 0.15, 100)
})

# ---- 위젯 영역 ----
st.subheader('필터 설정')

# 슬라이더로 표시할 행 수 조절
num_rows = st.slider('표시할 행 수', min_value=10, max_value=100, value=30, step=10)

# 컬럼 선택
selected_column = st.selectbox('차트에 표시할 컬럼', ['매출', '방문자', '전환율'])

# ---- 차트 표시 ----
filtered_df = df.head(num_rows)

st.subheader(f'{selected_column} 추이 차트')
st.line_chart(filtered_df.set_index('날짜')[selected_column])

# 요약 지표
col1, col2, col3 = st.columns(3)
col1.metric("최대", f"{filtered_df[selected_column].max():.2f}")
col2.metric("평균", f"{filtered_df[selected_column].mean():.2f}")
col3.metric("최소", f"{filtered_df[selected_column].min():.2f}")

# ---- 원본 데이터 (checkbox로 표시/숨김) ----
if st.checkbox('원본 데이터 보기'):
    st.dataframe(filtered_df)
