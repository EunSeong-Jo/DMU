# caching_demo.py
import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="캐싱 실전", layout="wide")
st.title('⚡ 캐싱 전 vs 후 속도 비교')

# ---- 캐싱 없는 함수 ----
def load_data_slow():
    """매번 2초가 걸리는 데이터 로딩 (캐싱 없음)"""
    time.sleep(2)  # 느린 데이터 로딩을 시뮬레이션
    np.random.seed(42)
    return pd.DataFrame({
        '날짜': pd.date_range('2025-01-01', periods=1000),
        '매출': np.random.randint(100, 10000, 1000),
        '카테고리': np.random.choice(['식품', '전자', '의류', '도서'], 1000)
    })

# ---- 캐싱 있는 함수 ----
@st.cache_data(show_spinner="데이터를 불러오는 중...")
def load_data_fast():
    """첫 실행만 2초, 이후는 즉시 반환 (캐싱 있음)"""
    time.sleep(2)
    np.random.seed(42)
    return pd.DataFrame({
        '날짜': pd.date_range('2025-01-01', periods=1000),
        '매출': np.random.randint(100, 10000, 1000),
        '카테고리': np.random.choice(['식품', '전자', '의류', '도서'], 1000)
    })

# ---- 비교 실행 ----
col1, col2 = st.columns(2)

with col1:
    st.subheader('❌ 캐싱 없음')
    if st.button('데이터 로딩 (느림)', key='slow'):
        start = time.time()
        df = load_data_slow()
        elapsed = time.time() - start
        st.metric('소요 시간', f'{elapsed:.2f}초')
        st.dataframe(df.head(5))

with col2:
    st.subheader('✅ 캐싱 있음')
    if st.button('데이터 로딩 (빠름)', key='fast'):
        start = time.time()
        df = load_data_fast()
        elapsed = time.time() - start
        st.metric('소요 시간', f'{elapsed:.2f}초')
        st.dataframe(df.head(5))

st.info('💡 캐싱 있는 버전은 두 번째 클릭부터 즉시 반환됩니다. 위젯을 조작해도 캐싱된 데이터는 유지됩니다.')

# 코드 설명:
# time.time()      → 현재 시각을 초 단위 숫자로 반환 (예: 1711300000.123)
# elapsed          → 끝 시각 - 시작 시각 = 소요 시간(초)
# f'{elapsed:.2f}' → 소수점 2자리까지 표시 (예: "2.01")

# ---- 사이드바: 위젯 조작으로 재실행 유도 ----
st.sidebar.header('필터 (위젯 조작 = 재실행)')
category = st.sidebar.selectbox('카테고리', ['전체', '식품', '전자', '의류', '도서'])
st.sidebar.write(f'선택: {category}')
st.sidebar.warning('⬆ 카테고리를 바꿔보세요. 캐싱 없는 쪽은 매번 느려집니다.')
