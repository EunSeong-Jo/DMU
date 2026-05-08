# app.py (Streamlit)
import streamlit as st
import pandas as pd

st.title('학생 성적표')

df = pd.DataFrame({'이름': ['김철수', '이영희'], '점수': [85, 92]})
st.dataframe(df)
st.bar_chart(df.set_index('이름'))
