# write_demo.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('st.write() 만능 출력기')

# 1. 문자열 → 텍스트로 출력
st.write('안녕하세요, Streamlit!')

# 2. 숫자 → 그대로 출력
st.write(42)
st.write(3.14)

# 3. 마크다운 → 렌더링
st.write('## 이것은 제목입니다')
st.write('**굵은 글씨**, *기울임*, `코드`')

# 4. DataFrame → 인터랙티브 테이블
df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수'],
    '국어': [90, 85, 78],
    '영어': [88, 92, 95],
    '수학': [76, 88, 90]
})
st.write(df)

# 5. 딕셔너리 → JSON 형태
st.write({'이름': '김철수', '나이': 22, '전공': '컴퓨터공학'})

# 6. 리스트 → 배열 형태
st.write([1, 2, 3, 4, 5])

# 7. 여러 인자를 한번에
st.write('김철수의 점수는', 90, '점입니다')
