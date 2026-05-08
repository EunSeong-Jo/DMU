import ollama

# 가장 기본적인 텍스트 생성
response = ollama.generate(
    model="gemma3:1b",
    prompt="파이썬이란 무엇인가요? 한 문장으로 설명해주세요."
)

# 결과 확인
print(response["response"])
