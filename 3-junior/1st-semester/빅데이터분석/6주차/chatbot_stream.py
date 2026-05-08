import streamlit as st
import ollama

st.title("Ollama 스트리밍 챗봇")

# ── 1. 대화 기록 초기화 ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── 2. 기존 대화 기록 표시 ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 3. 사용자 입력 처리 ──
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    # 사용자 메시지 추가 & 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # ── 4. 스트리밍 응답 ──
    with st.chat_message("assistant"):
        # Ollama 스트리밍 호출
        stream = ollama.chat(
            model="gemma3:4b",
            messages=st.session_state.messages,
            stream=True
        )

        # 제너레이터 함수로 변환
        def stream_generator():
            for chunk in stream:
                yield chunk["message"]["content"]

        # st.write_stream으로 실시간 표시 (내부적으로 모든 조각을 이어 붙여 전체 텍스트를 반환)
        full_response = st.write_stream(stream_generator())

    # ── 5. 완성된 응답을 기록에 추가 ──
    st.session_state.messages.append({"role": "assistant", "content": full_response})
