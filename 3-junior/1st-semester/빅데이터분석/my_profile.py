# my_profile.py
import streamlit as st
import pandas as pd

st.title('자기소개')

# 본인 정보 수정하기!
st.write('## 기본 정보')
st.write('**이름** : 조은성')
st.write('**학과** :인공지능소프트웨어학과')
st.write('**학년** : 3학년')
st.write('---') # 구분선
st.write('## 이번 학기 시간표')

schedule = pd.DataFrame({
 '요일': ['월', '화', '수', '목', '금'],

 '2교시': ['라이브러리', '-', '-', '-', '자연어'],
 
 '3교시': ['라이브러리', '-', '-', '-', '자연어'],
 
 '4교시': ['라이브러리', '-', '-', '-', '자연어'],

 '5교시': ['-', '-', '-', '-', '-'],

 '6교시': ['-', '캡스톤', '-', '서비스', '빅데이터분석'],

 '7교시': ['-', '캡스톤', '-', '서비스', '빅데이터분석'],

 '8교시': ['-', '캡스톤', '-', '서비스', '빅데이터분석'],

 '9교시': ['-', '캡스톤', '-', '-', '-']
})

st.write(schedule)
st.write('---')
st.write('## 관심 분야')
st.write('- 데이터 분석')
st.write('- 데이터 시각화')
st.write('- 머신러닝 & 딥러닝')
st.write('---')
st.write('## 이번 학기 목표')

goals = pd.DataFrame({
 '목표': ['Streamlit 마스터', 'HuggingFace 활용', '포트폴리오 완성'],
 '달성률': [2, 1, 3]
})

st.write(goals)
st.bar_chart(goals.set_index('목표'))
