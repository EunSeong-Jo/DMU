# cart_demo.py
import streamlit as st

st.title('🛒 장바구니')

# 초기화
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 상품 추가
product = st.selectbox('상품 선택', ['노트북', '마우스', '키보드', '모니터', '헤드셋'])
if st.button('장바구니에 추가'):
    st.session_state.cart.append(product)
    st.toast(f'{product} 추가됨!')

# 장바구니 표시
if st.session_state.cart:
    st.subheader(f'장바구니 ({len(st.session_state.cart)}개)')
    for i, item in enumerate(st.session_state.cart):
        col1, col2 = st.columns([4, 1])
        col1.write(f'{i+1}. {item}')
        if col2.button('삭제', key=f'del_{i}'):
            st.session_state.cart.pop(i)
            st.rerun()

    if st.button('🗑️ 전체 비우기'):
        st.session_state.cart = []
        st.rerun()
else:
    st.info('장바구니가 비어있습니다.')
