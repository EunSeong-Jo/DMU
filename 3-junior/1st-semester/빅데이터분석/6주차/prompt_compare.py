import ollama

# 나쁜 프롬프트: 모호하고 불명확
bad_prompt = "파이썬에 대해 알려줘"

# 좋은 프롬프트: 구체적이고 명확
good_prompt = """당신은 대학교 프로그래밍 강사입니다.
프로그래밍 초보 대학생에게 파이썬의 장점을 설명해주세요.

조건:
- 3가지 장점을 각각 한 문장으로 설명
- 비유를 활용하여 쉽게 설명
- 마지막에 한 줄 요약 추가
"""

print("=" * 60)
print("나쁜 프롬프트")
print("=" * 60)
response = ollama.generate(model="gemma3:4b", prompt=bad_prompt)
print(response["response"][:300])  # 앞 300자만

print("\n" + "=" * 60)
print("좋은 프롬프트")
print("=" * 60)
response = ollama.generate(model="gemma3:4b", prompt=good_prompt)
print(response["response"])
