# sidebar_demo.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('사이드바 레이아웃')

# ---- 사이드바에 위젯 배치 ----
st.sidebar.header('필터 설정')

# 방법 1: st.sidebar.위젯명()
category = st.sidebar.selectbox('카테고리', ['전자제품', '의류', '식품'])
num_rows = st.sidebar.slider('표시 행 수', 10, 100, 30)

# 방법 2: with 구문 (여러 위젯을 묶을 때 편리)
with st.sidebar:
    st.write('---')
    show_raw = st.checkbox('원본 데이터 보기')

# ---- 메인 영역 ----
st.subheader(f'{category} 데이터')
df = pd.DataFrame(np.random.randn(num_rows, 3), columns=['A', 'B', 'C'])
st.line_chart(df)

if show_raw:
    st.dataframe(df)
