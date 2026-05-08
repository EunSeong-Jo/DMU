# expander_demo.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('Expander 레이아웃')

# 기본 사용법
with st.expander('상세 설명 보기'):
    st.write('이 영역은 접었다 펼 수 있습니다.')
    st.write('긴 설명이나 부가 정보를 넣기 좋습니다.')
    st.code('with st.expander("제목"):\n    st.write("내용")')

# 실전 패턴: 데이터 숨기기
st.subheader('매출 추이')
df = pd.DataFrame(
    np.random.randint(100, 500, (20, 3)),
    columns=['매출', '비용', '이익']
)
st.line_chart(df)

with st.expander('원본 데이터 확인'):
    st.dataframe(df)
