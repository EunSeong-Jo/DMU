# tabs_demo.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('탭 레이아웃')

# 탭 생성
tab1, tab2, tab3 = st.tabs(['차트', '데이터', '설명'])

df = pd.DataFrame(np.random.randn(50, 3), columns=['매출', '비용', '이익'])

with tab1:
    st.subheader('추이 차트')
    st.line_chart(df)

with tab2:
    st.subheader('원본 데이터')
    st.dataframe(df)

with tab3:
    st.subheader('분석 설명')
    st.write("""
    - **매출**: 랜덤 정규분포 데이터
    - **비용**: 랜덤 정규분포 데이터
    - **이익**: 랜덤 정규분포 데이터

    > 이 데이터는 실습용 더미 데이터입니다.
    """)
