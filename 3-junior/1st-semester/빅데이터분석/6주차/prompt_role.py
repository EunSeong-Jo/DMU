import ollama

# 같은 질문, 다른 역할
question = "인공지능이 일자리를 빼앗을까요?"

roles = [
    "당신은 IT 기업의 CEO입니다.",
    "당신은 경제학 교수입니다.",
    "당신은 공장 노동자입니다."
]

for role in roles:
    print(f"\n{'=' * 50}")
    print(f"역할: {role}")
    print("=" * 50)

    response = ollama.chat(
        model="gemma3:1b",
        messages=[
            {"role": "system", "content": f"{role} 2~3문장으로 답변해주세요."},
            {"role": "user", "content": question}
        ]
    )
    print(response["message"]["content"])
