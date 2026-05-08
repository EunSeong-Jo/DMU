# callback_demo.py
import streamlit as st

st.title('콜백 실시간 반응')

# 콜백 함수 정의
def update_greeting():
    name = st.session_state.user_name
    st.session_state.greeting = f'안녕하세요, {name}님! 👋' if name else ''

def calculate_bmi():
    h = st.session_state.height / 100  # cm → m
    w = st.session_state.weight
    st.session_state.bmi = w / (h * h)

# 이름 입력 → 즉시 인사말 업데이트
st.text_input('이름', key='user_name', on_change=update_greeting)
if 'greeting' in st.session_state and st.session_state.greeting:
    st.write(st.session_state.greeting)

st.divider()

# BMI 계산기 (슬라이더 조작 시 즉시 계산)
st.subheader('BMI 계산기')
st.slider('키 (cm)', 140, 200, 170, key='height', on_change=calculate_bmi)
st.slider('몸무게 (kg)', 30, 150, 70, key='weight', on_change=calculate_bmi)

if 'bmi' in st.session_state:
    bmi = st.session_state.bmi
    if bmi < 18.5:
        status = '저체중'
    elif bmi < 25:
        status = '정상'
    elif bmi < 30:
        status = '과체중'
    else:
        status = '비만'
    st.metric('BMI', f'{bmi:.1f}', status)
