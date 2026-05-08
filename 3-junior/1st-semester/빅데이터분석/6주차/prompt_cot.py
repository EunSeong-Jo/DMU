import ollama

# ❌ CoT 없이 바로 답 요청
bad = "한 상자에 사과가 12개 있고, 3상자를 사서 친구 4명에게 똑같이 나눠주면 한 명당 몇 개?"

# ✅ CoT로 단계별 사고 요청
good = """한 상자에 사과가 12개 있고, 3상자를 사서 친구 4명에게 똑같이 나눠주면 한 명당 몇 개?

단계별로 풀어주세요:
1. 전체 사과 수 계산
2. 나눠줄 인원 확인
3. 한 명당 개수 계산
"""

# 두 방식을 비교해보자
print("❌ CoT 없이:")
print("=" * 40)
response = ollama.generate(model="gemma3:1b", prompt=bad)
print(response["response"])

print("\n✅ CoT 사용:")
print("=" * 40)
response = ollama.generate(model="gemma3:1b", prompt=good)
print(response["response"])
