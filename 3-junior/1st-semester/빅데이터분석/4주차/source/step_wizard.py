# step_wizard.py
import streamlit as st

st.set_page_config(page_title="단계별 입력", page_icon="📝")
st.title('📝 단계별 정보 입력')

# ---- 상태 초기화 ----
if 'step' not in st.session_state:
    st.session_state.step = 1

# ---- 진행률 표시 ----
progress = st.session_state.step / 3
st.progress(progress, text=f'Step {st.session_state.step} / 3')

# ---- Step 1: 기본 정보 ----
if st.session_state.step == 1:
    st.subheader('Step 1: 기본 정보')
    name = st.text_input('이름', key='name')
    age = st.number_input('나이', min_value=1, max_value=100, value=20, key='age')

    if st.button('다음 →'):
        if name:  # 이름이 입력되었는지 확인
            st.session_state.step = 2
            st.session_state.saved_name = name  # 위젯 key와 별도로 저장
            st.session_state.saved_age = age    # 위젯 key와 별도로 저장
            st.rerun()  # 페이지 즉시 갱신
        else:
            st.warning('이름을 입력해주세요.')

# ---- Step 2: 관심 분야 ----
elif st.session_state.step == 2:
    st.subheader('Step 2: 관심 분야')
    interests = st.multiselect(
        '관심 분야를 선택하세요',
        ['데이터 분석', '웹 개발', 'AI/ML', '모바일', '게임', '보안'],
        key='interests'
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← 이전'):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button('다음 →'):
            st.session_state.step = 3
            st.rerun()

# ---- Step 3: 확인 ----
elif st.session_state.step == 3:
    st.subheader('Step 3: 입력 확인')
    st.write(f"**이름**: {st.session_state.get('saved_name', '')}")
    st.write(f"**나이**: {st.session_state.get('saved_age', '')}")
    st.write(f"**관심 분야**: {', '.join(st.session_state.get('interests', []))}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button('← 이전'):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button('✅ 제출'):
            st.balloons()
            st.success('제출이 완료되었습니다!')
            # 초기화
            for key in ['step', 'name', 'age', 'interests']:
                if key in st.session_state:
                    del st.session_state[key]
