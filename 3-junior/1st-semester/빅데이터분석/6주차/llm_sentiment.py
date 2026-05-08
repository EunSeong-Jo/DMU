import ollama

reviews = [
    "이 영화 정말 재미있었어요! 배우들 연기도 훌륭하고 스토리도 감동적이었습니다.",
    "시간 낭비했어요. 스토리도 엉망이고 연기도 어색했습니다.",
    "그냥 그랬어요. 나쁘지는 않은데 특별히 좋지도 않았어요.",
    "OST가 정말 좋았어요! 그런데 결말이 좀 아쉬웠네요."
]

for review in reviews:
    response = ollama.chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "system",
                "content": "당신은 감성 분석 전문가입니다. 주어진 리뷰의 감성을 '긍정', '부정', '중립' 중 하나로 분류하고, 이유를 한 문장으로 설명해주세요."
            },
            {
                "role": "user",
                "content": f"다음 리뷰를 분석해주세요: {review}"
            }
        ]
    )
    print(f"리뷰: {review[:30]}...")
    print(f"분석: {response['message']['content']}")
    print("-" * 60)
