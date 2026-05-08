import ollama

# 표 형식으로 출력 요청
response = ollama.chat(
    model="gemma3:4b",
    messages=[
        {"role": "system", "content": "답변은 반드시 마크다운 표 형식으로 작성하세요."},
        {"role": "user", "content": "Python, Java, JavaScript의 특징을 비교해주세요. 항목: 타입, 용도, 난이도"}
    ]
)
print(response["message"]["content"])
