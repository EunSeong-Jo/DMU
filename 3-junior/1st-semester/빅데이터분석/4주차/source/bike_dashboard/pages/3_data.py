# pages/3_data.py
import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import load_bike_data, get_station_summary, load_raw_data

st.title('🔍 데이터 조회')

df = load_bike_data()
summary = get_station_summary(df)

tab1, tab2 = st.tabs(['대여소 요약', '원본 데이터'])

with tab1:
    st.subheader('대여소별 요약 통계')

    # 행 선택 가능한 데이터프레임
    event = st.dataframe(
        summary,
        on_select="rerun",
        selection_mode="multi-row",
        use_container_width=True,
        column_config={
            '총대여건수': st.column_config.NumberColumn(format="%d 건"),
            '평균이용시간': st.column_config.NumberColumn(format="%.1f 분"),
            '일평균대여': st.column_config.ProgressColumn(
                min_value=0,
                max_value=summary['일평균대여'].max(),
                format="%.0f건/일"
            )
        }
    )

    # 선택한 대여소 상세 정보
    selected = event.selection.rows
    if selected:
        selected_stations = summary.iloc[selected]['대여소'].tolist()
        st.subheader(f'선택한 대여소: {", ".join(selected_stations)}')

        detail = df[df['대여소'].isin(selected_stations)]
        monthly_detail = detail.groupby(['대여소', '날짜'])['대여건수'].sum().reset_index()

        import plotly.express as px
        fig = px.line(monthly_detail, x='날짜', y='대여건수',
                      color='대여소', markers=True,
                      title='선택 대여소 월별 대여 추이')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader('원본 데이터')

    # 원본 CSV 데이터 로딩 (집계 전 전체 컬럼)
    raw_df = load_raw_data()

    if raw_df.empty:
        st.warning('원본 CSV 데이터를 불러올 수 없습니다. 집계된 데이터를 표시합니다.')
        raw_df = df

    # 컬럼 선택
    all_columns = raw_df.columns.tolist()
    selected_columns = st.multiselect(
        '표시할 컬럼 선택',
        all_columns,
        default=all_columns,
        key='column_selector'
    )

    if not selected_columns:
        st.warning('컬럼을 1개 이상 선택하세요.')
    else:
        # Form으로 필터 모아서 적용
        with st.form('data_filter'):
            col1, col2 = st.columns(2)
            with col1:
                station_col = '대여소명' if '대여소명' in raw_df.columns else '대여소'
                station_filter = st.multiselect(
                    '대여소', raw_df[station_col].unique(),
                    default=raw_df[station_col].unique()
                )
            with col2:
                date_col = '대여일자' if '대여일자' in raw_df.columns else '날짜'
                date_options = sorted(raw_df[date_col].astype(str).unique())
                month_filter = st.multiselect('월 선택', date_options, default=date_options)

            submitted = st.form_submit_button('필터 적용', use_container_width=True)

        filtered = raw_df[
            (raw_df[station_col].isin(station_filter)) &
            (raw_df[date_col].astype(str).isin(month_filter))
        ][selected_columns]

        st.write(f'검색 결과: **{len(filtered):,}건** / 전체 {len(raw_df):,}건 | 컬럼: {len(selected_columns)}개')
        st.dataframe(filtered, use_container_width=True, height=400)

        # CSV 다운로드
        csv = filtered.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label='📥 CSV 다운로드',
            data=csv,
            file_name='bike_data_filtered.csv',
            mime='text/csv'
        )
