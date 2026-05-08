import streamlit as st

st.title("채팅 UI 테스트")

# 채팅 메시지 표시
with st.chat_message("user"):
    st.write("Streamlit으로 챗봇을 만들 수 있나요?")

with st.chat_message("assistant"):
    st.write("네, 물론이죠! st.chat_message와 st.chat_input을 사용하면 됩니다.")

with st.chat_message("user"):
    st.write("어렵지 않나요?")

with st.chat_message("assistant"):
    st.write("전혀요! 지금부터 함께 만들어 봅시다.")

# 하단 입력창
user_input = st.chat_input("메시지를 입력하세요")
if user_input:
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(f"'{user_input}'라고 하셨군요!")
