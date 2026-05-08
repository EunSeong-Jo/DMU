import ollama

# 대화형 API — 메시지 목록을 전달
response = ollama.chat(
    model="gemma3:1b",
    messages=[
        {
            "role": "user",
            "content": "빅데이터의 3V에 대해 설명해주세요."
        }
    ]
)

# 응답 출력
print(response["message"]["content"])
