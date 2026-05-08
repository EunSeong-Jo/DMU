import ollama

print("스트리밍 출력 시작:")
print("-" * 40)

# stream=True로 실시간 출력
stream = ollama.chat(
    model="gemma3:1b",
    messages=[
        {"role": "user", "content": "Streamlit이 무엇인지 5줄로 설명해주세요."}
    ],
    stream=True
)

for chunk in stream:
    # 각 청크에서 텍스트 조각을 추출하여 출력
    print(chunk["message"]["content"], end="", flush=True)

print()  # 마지막 줄바꿈
