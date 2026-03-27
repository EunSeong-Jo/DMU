import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="빅데이터 분석 프로젝트", page_icon="📊")

# 제목
st.title("빅데이터 분석 프로젝트")
st.write("첫 번째 Streamlit 앱입니다!")

# 구분선
st.divider()

# 간단한 데이터프레임 표시
st.subheader("샘플 데이터")
data = {
    "이름": ["김철수", "이영희", "박민수", "정수진", "최지훈"],
    "학년": [3, 3, 3, 3, 3],
    "전공": ["AI소프트웨어", "AI소프트웨어", "AI소프트웨어", "AI소프트웨어", "AI소프트웨어"],
    "Python점수": [85, 92, 78, 95, 88]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# 간단한 차트
st.subheader("Python 점수 차트")
st.bar_chart(df.set_index("이름")["Python점수"])

# 사이드바
st.sidebar.header("설정")
st.sidebar.write("이 영역은 사이드바입니다.")
name = st.sidebar.text_input("이름을 입력하세요")
if name:
    st.sidebar.write(f"안녕하세요, {name}님!")