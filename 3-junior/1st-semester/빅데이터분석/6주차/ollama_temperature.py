import ollama

prompt = "인공지능의 미래에 대해 한 문장으로 말해주세요."

print("=" * 60)
print("Temperature 비교 실험")
print("=" * 60)

for temp in [0.0, 0.7, 1.5]:
    print(f"\n--- Temperature = {temp} ---")
    for i in range(3):
        response = ollama.generate(
            model="gemma3:1b",
            prompt=prompt,
            options={"temperature": temp}
        )
        answer = response["response"].strip().split("\n")[0]  # 첫 줄만
        print(f"  시도 {i+1}: {answer}")
