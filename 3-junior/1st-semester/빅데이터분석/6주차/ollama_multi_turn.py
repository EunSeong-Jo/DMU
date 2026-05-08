import ollama

# 시스템 프롬프트로 AI의 역할 설정
messages = [
    {
        "role": "system",
        "content": "당신은 친절한 파이썬 튜터입니다. 대학생 눈높이에 맞춰 쉽게 설명해주세요. 답변은 3문장 이내로 간결하게 해주세요."
    },
    {
        "role": "user",
        "content": "리스트와 튜플의 차이가 뭐예요?"
    }
]

# 첫 번째 질문
response = ollama.chat(model="gemma3:1b", messages=messages)
assistant_reply = response["message"]["content"]
print("AI:", assistant_reply)

# AI의 답변을 대화 기록에 추가
messages.append({"role": "assistant", "content": assistant_reply})

# 두 번째 질문 (이전 대화를 기억함)
messages.append({"role": "user", "content": "그러면 딕셔너리는요?"})
response = ollama.chat(model="gemma3:1b", messages=messages)
print("\nAI:", response["message"]["content"])
