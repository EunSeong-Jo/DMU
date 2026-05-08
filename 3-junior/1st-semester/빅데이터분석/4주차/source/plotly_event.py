# plotly_event.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Plotly 이벤트", layout="wide")
st.title('🖱️ 차트 클릭 → 상세 정보')

# ---- 데이터 ----
np.random.seed(42)
df = pd.DataFrame({
    '도시': ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종'],
    '인구(만)': [970, 340, 240, 295, 145, 150, 114, 38],
    '면적(km²)': [605, 770, 884, 1063, 501, 540, 1062, 465],
    '평균기온(°C)': [12.5, 14.7, 14.1, 12.1, 13.8, 13.0, 14.3, 12.4]
})

# ---- 산점도: 인구 vs 면적 ----
fig = px.scatter(df, x='면적(km²)', y='인구(만)',
                 size='인구(만)', color='평균기온(°C)',
                 hover_name='도시',
                 title='도시별 인구 vs 면적',
                 color_continuous_scale='Viridis')

# on_select="rerun" → 사용자가 점을 클릭하면 Streamlit이 재실행됨
event = st.plotly_chart(fig, on_select="rerun", use_container_width=True)

# ---- 선택된 데이터 표시 ----
if event and event.selection and event.selection.points:
    selected_points = event.selection.points
    st.subheader('선택한 도시 정보')
    for point in selected_points:
        idx = point['point_index']
        city = df.iloc[idx]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('도시', city['도시'])
        col2.metric('인구', f"{city['인구(만)']}만 명")
        col3.metric('면적', f"{city['면적(km²)']} km²")
        col4.metric('평균기온', f"{city['평균기온(°C)']}°C")
else:
    st.info('💡 차트에서 점을 클릭하면 해당 도시의 상세 정보가 표시됩니다. (Box Select 또는 Lasso Select 도구로 여러 점을 선택할 수도 있습니다)')
