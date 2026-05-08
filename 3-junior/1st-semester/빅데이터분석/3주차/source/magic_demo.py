# magic_demo.py
import streamlit as st
import pandas as pd

st.title('Magic Commands 체험')

# 방법 1: st.write() 사용
df = pd.DataFrame({
    '과목': ['국어', '영어', '수학'],
    '점수': [90, 85, 95]
})
st.write(df)  # 명시적 호출

# 방법 2: Magic! - 변수명만 적으면 자동 출력
df2 = pd.DataFrame({
    '과목': ['과학', '사회', '역사'],
    '점수': [88, 76, 92]
})
df2  # st.write(df2)와 동일한 결과!

# 방법 3: 삼중 따옴표 마크다운도 Magic으로 렌더링
"""
## 오늘의 분석 결과
- 매출이 전월 대비 **15% 증가**
- 신규 고객 수 *200명* 달성
> 전반적으로 긍정적인 추세입니다.
"""
