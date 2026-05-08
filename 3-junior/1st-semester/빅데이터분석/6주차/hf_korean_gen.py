from transformers import pipeline

# 한국어 텍스트 생성 파이프라인
generator = pipeline(
    "text-generation",
    model="skt/ko-gpt-trinity-1.2B-v0.5",
    device="cpu"  # GPU가 있으면 device=0
)

# 텍스트 생성
result = generator(
    "인공지능 기술이 발전하면서",
    max_new_tokens=100,      # 최대 생성 토큰 수
    temperature=0.7,         # 창의성 조절
    do_sample=True,          # 샘플링 활성화 (temperature 사용 시 필수)
    repetition_penalty=1.2   # 반복 방지
)

print("생성된 텍스트:")
print(result[0]["generated_text"])
