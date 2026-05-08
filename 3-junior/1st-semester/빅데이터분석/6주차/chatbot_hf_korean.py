import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="한국어 AI 챗봇", page_icon="🇰🇷")
st.title("HuggingFace 한국어 텍스트 생성 챗봇")
st.caption("skt/ko-gpt-trinity-1.2B-v0.5 모델 사용")

# ── 모델 로딩 (캐싱) ──
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="skt/ko-gpt-trinity-1.2B-v0.5",
        device="cpu"
    )

with st.spinner("모델 로딩 중... (최초 1회만 소요)"):
    generator = load_model()

# ── 사이드바 설정 ──
with st.sidebar:
    st.header("생성 설정")
    max_tokens = st.slider("최대 생성 토큰", 50, 300, 150)
    temperature = st.slider("Temperature", 0.1, 1.5, 0.7, 0.1)
    rep_penalty = st.slider("반복 방지 강도", 1.0, 2.0, 1.2, 0.1)

    st.divider()
    st.markdown("""
    **이 모델의 특징:**
    - 한국어 텍스트를 이어서 생성
    - "질문→답변" 대화보다는 문장 완성에 적합
    - 입력 텍스트를 시작점으로 글을 이어 씀
    """)

    if st.button("대화 초기화", use_container_width=True):
        st.session_state.hf_messages = []
        st.rerun()

# ── 대화 기록 ──
if "hf_messages" not in st.session_state:
    st.session_state.hf_messages = []

for msg in st.session_state.hf_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 사용자 입력 ──
user_input = st.chat_input("문장을 입력하면 AI가 이어서 작성합니다")

if user_input:
    st.session_state.hf_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("텍스트 생성 중..."):
            result = generator(
                user_input,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                repetition_penalty=rep_penalty
            )
            generated = result[0]["generated_text"]

            # text-generation 모델은 "입력 텍스트 + 생성된 텍스트"를 합쳐서 반환함
            # 예: "오늘 날씨가" 입력 → "오늘 날씨가 좋아서 공원에 갔다" 반환
            # → 입력 부분을 잘라내야 새로 생성된 부분만 사용자에게 보여줄 수 있음
            if generated.startswith(user_input):
                new_text = generated[len(user_input):]
            else:
                new_text = generated

            st.write(new_text)

    st.session_state.hf_messages.append({"role": "assistant", "content": new_text})
