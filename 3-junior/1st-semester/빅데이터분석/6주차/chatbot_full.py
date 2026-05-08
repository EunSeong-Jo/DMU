import streamlit as st
import ollama

# ── 페이지 설정 ──
st.set_page_config(page_title="AI 챗봇", page_icon="🤖", layout="wide")

# ── 사이드바: 설정 ──
with st.sidebar:
    st.header("챗봇 설정")

    # 시스템 프롬프트 선택
    system_prompts = {
        "일반 대화": "당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요.",
        "파이썬 튜터": "당신은 친절한 파이썬 프로그래밍 튜터입니다. 대학생 눈높이에 맞춰 쉽게 설명하고, 코드 예시를 포함해주세요.",
        "데이터 분석가": "당신은 데이터 분석 전문가입니다. Pandas, 시각화, 통계 분석에 대해 전문적으로 답변해주세요.",
        "영어 선생님": "당신은 영어 회화 선생님입니다. 사용자가 한국어로 질문하면 영어로 답변하고, 한국어 해설을 아래에 추가해주세요.",
        
        "인공지능 실무자" : "당신은 IT회사에서 인공지능을 활용해 바이브코딩으로 프로젝트를 진행하는 실무자 입니다. 질문하는 프로젝트에 대해 여러가지 MCP, Plugin 추천 및 사용방법에 대해 설명해주고 Claude Code, Gemini, ChatGPT Codex 등 여러 인공지능 도구들을 추천해주세요.",
        "분신술" : "자네는 나의 분신이라네. 나의 모든 것을 똑같이 행동하고 똑같이 생각하는 나의 복사본이라고 생각하면된다네."
    }

    selected_role = st.selectbox("AI 역할 선택", list(system_prompts.keys()))

    # 직접 입력 옵션
    custom_prompt = st.text_area(
        "또는 직접 입력:",
        placeholder="AI에게 부여할 역할을 입력하세요...",
        height=100
    )

    # Temperature 조절 (Ollama의 options 파라미터로 전달됨)
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)

    st.divider()

    # 대화 초기화 버튼
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # 대화 통계
    if "messages" in st.session_state:
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.caption(f"대화 수: {user_msgs}턴")

# ── 시스템 프롬프트 결정 ──
system_prompt = custom_prompt.strip() if custom_prompt.strip() else system_prompts[selected_role]

# ── 메인 화면 ──
st.title("AI 챗봇")
st.caption(f"현재 역할: {selected_role} | Temperature: {temperature}")

# ── 대화 기록 초기화 ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── 기존 대화 표시 ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 사용자 입력 ──
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Ollama에 전달할 메시지 (시스템 프롬프트 + 대화 기록)
    ollama_messages = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages

    with st.chat_message("assistant"):
        stream = ollama.chat(
            model="gemma3:1b",
            messages=ollama_messages,
            stream=True,
            options={"temperature": temperature}  # options: Ollama 모델 동작 제어 (temperature, top_k, top_p 등을 딕셔너리로 전달)
        )

        def stream_generator():
            for chunk in stream:
                yield chunk["message"]["content"]

        full_response = st.write_stream(stream_generator())

    st.session_state.messages.append({"role": "assistant", "content": full_response})
