# widget_demo.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('위젯 실습')

# ---- 1. selectbox: 드롭다운 선택 ----
st.subheader('1. selectbox — 드롭다운 선택')

category = st.selectbox(
    '카테고리를 선택하세요',
    ['전자제품', '의류', '식품', '도서']
)

st.write(f'선택한 카테고리: **{category}**')

# 선택에 따라 다른 데이터 표시
data = {
    '전자제품': {'평균가격': '₩35만', '판매량': 150},
    '의류':     {'평균가격': '₩5만',  '판매량': 320},
    '식품':     {'평균가격': '₩1만',  '판매량': 890},
    '도서':     {'평균가격': '₩2만',  '판매량': 210},
}

info = data[category]
st.write(f"평균 가격: {info['평균가격']}")
st.write(f"월 판매량: {info['판매량']}개")

st.divider()

# ---- 2. slider: 범위 조절 ----
st.subheader('2. slider — 범위 조절')

# 기본 슬라이더
age = st.slider('나이를 선택하세요', 0, 100, 25)
st.write(f'선택한 나이: {age}세')

# 범위 슬라이더 (튜플 반환)
price_range = st.slider(
    '가격 범위를 설정하세요',
    min_value=0,
    max_value=100000,
    value=(20000, 80000),   # 기본값을 튜플로 주면 범위 슬라이더
    step=5000,
    format='₩%d'
)
st.write(f'선택 범위: ₩{price_range[0]:,} ~ ₩{price_range[1]:,}')

st.divider()

# ---- 3. checkbox: 데이터 표시/숨김 ----
st.subheader('3. checkbox — 데이터 표시/숨김')

df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

# 차트는 항상 표시
st.line_chart(df)

# 체크박스로 원본 데이터 표시/숨김
if st.checkbox('원본 데이터 보기'):
    st.dataframe(df)

st.divider()

# ---- 4. radio: 라디오 버튼 ----
st.subheader('4. radio — 라디오 버튼')

chart_type = st.radio(
    '차트 종류를 선택하세요',
    ['선 차트', '바 차트', '영역 차트']
)

if chart_type == '선 차트':
    st.line_chart(df)
elif chart_type == '바 차트':
    st.bar_chart(df)
else:
    st.area_chart(df)

st.divider()

# ---- 5. multiselect: 다중 선택 ----
st.subheader('5. multiselect — 다중 선택')

columns = st.multiselect(
    '표시할 컬럼을 선택하세요',
    ['A', 'B', 'C'],
    default=['A', 'B']
)

if columns:
    st.line_chart(df[columns])
else:
    st.write('컬럼을 하나 이상 선택하세요.')
