import ollama

# 리뷰 → 카테고리 분류를 Few-shot으로
fewshot_prompt = """다음은 상품 리뷰를 카테고리로 분류하는 예시입니다.

리뷰: "배송이 너무 빨라서 좋았어요"
카테고리: 배송

리뷰: "가격 대비 품질이 좋습니다"
카테고리: 품질

리뷰: "고객센터 응대가 친절했습니다"
카테고리: 서비스

리뷰: "포장이 꼼꼼하게 되어 있었어요"
카테고리: 배송

이제 다음 리뷰를 분류해주세요. 카테고리만 답하세요.

리뷰: "사용법을 물어봤는데 자세히 알려줘서 감사합니다"
카테고리:"""

response = ollama.generate(model="gemma3:4b", prompt=fewshot_prompt)
print("분류 결과:", response["response"].strip())
