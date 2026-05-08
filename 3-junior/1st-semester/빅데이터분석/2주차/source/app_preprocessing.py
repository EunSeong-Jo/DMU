import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="전처리 영향 분석", page_icon="📈")

# 한글 폰트 설정 (Matplotlib/Seaborn 한글 깨짐 방지)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

st.title("📊 데이터 전처리가 분석에 미치는 영향")
st.markdown("""
데이터 전처리는 단순히 깨끗하게 만드는 작업이 아닙니다. 
**왜곡된 데이터 속에 숨겨진 진실(상관계수)을 찾아내는 과정**입니다.
""")

# 1. 원본 데이터 생성
data = {
    "가격": [100, 120, 110, 130, 150, 140, 5000, 10, None, 135],
    "평점": [4.0, 4.2, 3.8, 4.3, 4.5, 4.1, 1.0, 5.0, 4.0, None]
}
df = pd.DataFrame(data)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 전처리 전 (Original)")
    st.write("이상치와 결측치가 포함된 데이터입니다.")
    st.dataframe(df.style.highlight_null(color='red'), use_container_width=True) # 결측치 강조
    
    # 전처리 전 상관계수
    corr_before = df.corr().iloc[0, 1]
    st.metric("상관계수", f"{corr_before:.2f}")

with col2:
    st.subheader("2. 전처리 후 (Cleaned)")
    
    # 전처리 로직 수행
    df_clean = df.copy()
    # 결측치 중앙값 대체
    df_clean["가격"] = df_clean["가격"].fillna(df_clean["가격"].median())
    df_clean["평점"] = df_clean["평점"].fillna(df_clean["평점"].median())

    # 이상치 제거 (IQR)
    def remove_outliers(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        return df[(df[column] >= lower) & (df[column] <= upper)]

    df_clean = remove_outliers(df_clean, "가격")
    df_clean = remove_outliers(df_clean, "평점")
    
    st.write("결측치를 채우고 이상치를 제거한 데이터입니다.")
    st.dataframe(df_clean, use_container_width=True)
    
    # 전처리 후 상관계수
    corr_after = df_clean.corr().iloc[0, 1]
    st.metric("상관계수", f"{corr_after:.2f}", delta=f"{corr_after - corr_before:.2f}")

st.divider()

# 3. 시각화 비교
st.subheader("🔍 시각적 비교 분석")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 전처리 전 산점도
sns.scatterplot(x="가격", y="평점", data=df, ax=axes[0], color='red', s=100)
axes[0].set_title(f"전처리 전 (r = {corr_before:.2f})")

# 전처리 후 산점도 + 회귀선
sns.regplot(x="가격", y="평점", data=df_clean, ax=axes[1], color='blue', scatter_kws={'s':100})
axes[1].set_title(f"전처리 후 (r = {corr_after:.2f})")

st.pyplot(fig) # Streamlit에 차트 출력

st.info(f"""
**분석 결과:**
전처리 전에는 이상치 때문에 관계가 **{corr_before:.2f}**로 매우 낮게 측정되었습니다.
전처리 후 이상치를 제거하자 실제 관계인 **{corr_after:.2f}**의 강한 양의 상관관계가 나타납니다.
""")