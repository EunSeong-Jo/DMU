# button_demo.py
import streamlit as st

st.title('위젯 실습 - button')

# 버튼 기본 패턴
if st.button('인사하기'):
    st.write('안녕하세요! 반갑습니다! 👋')
else:
    st.write('버튼을 눌러보세요.')

# 계산 버튼 패턴
st.title('계산기')

num1 = st.number_input('첫 번째 숫자', value=10)
num2 = st.number_input('두 번째 숫자', value=20)

operation = st.selectbox('연산 선택', ['더하기', '빼기', '곱하기', '나누기'])

if st.button('계산하기'):
    if operation == '더하기':
        result = num1 + num2
    elif operation == '빼기':
        result = num1 - num2
    elif operation == '곱하기':
        result = num1 * num2
    else:
        result = num1 / num2 if num2 != 0 else '0으로 나눌 수 없습니다'

    st.success(f'결과: {result}')
