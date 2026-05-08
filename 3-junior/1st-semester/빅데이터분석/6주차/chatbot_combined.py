import streamlit as st
import ollama
from transformers import pipeline

st.set_page_config(page_title="AI 챗봇 비교", page_icon="🤖", layout="wide")

# ── 사이드바 ──
with st.sidebar:
    st.header("설정")

    model_choice = st.radio(
        "모델 선택",
        ["Ollama (gemma3:4b)", "HuggingFace (한국어 생성)"],
        help="Ollama: 대화형 챗봇 / HuggingFace: 텍스트 이어쓰기"
    )

    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)

    if model_choice == "Ollama (gemma3:4b)":
        system_role = st.text_area(
            "시스템 프롬프트",
            value="당신은 친절한 AI 어시스턴트입니다. 한국어로 답변해주세요.",
            height=100
        )
    else:
        max_tokens = st.slider("최대 생성 토큰", 50, 300, 150)

    st.divider()

    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── HuggingFace 모델 캐싱 ──
@st.cache_resource
def load_hf_model():
    return pipeline(
        "text-generation",
        model="skt/ko-gpt-trinity-1.2B-v0.5",
        device="cpu"
    )

# ── 메인 화면 ──
st.title("AI 챗봇 비교")
st.caption(f"현재 모델: {model_choice}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        if model_choice == "Ollama (gemma3:4b)":
            # ── Ollama 스트리밍 ──
            ollama_messages = [
                {"role": "system", "content": system_role}
            ] + st.session_state.messages

            stream = ollama.chat(
                model="gemma3:4b",
                messages=ollama_messages,
                stream=True,
                options={"temperature": temperature}
            )

            def stream_gen():
                for chunk in stream:
                    yield chunk["message"]["content"]

            full_response = st.write_stream(stream_gen())

        else:
            # ── HuggingFace 한국어 생성 ──
            with st.spinner("텍스트 생성 중..."):
                gen = load_hf_model()
                result = gen(
                    user_input,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    repetition_penalty=1.2
                )
                generated = result[0]["generated_text"]
                full_response = generated[len(user_input):] if generated.startswith(user_input) else generated
                st.write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
