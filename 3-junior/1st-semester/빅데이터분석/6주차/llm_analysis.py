import ollama

article = """
인공지능(AI) 기술이 의료 분야에서 혁신을 이끌고 있다. 특히 의료 영상 분석에서
AI는 방사선 전문의보다 높은 정확도로 종양을 탐지하는 성과를 보이고 있다.
삼성서울병원은 AI 기반 폐암 조기 진단 시스템을 도입하여 진단 정확도를 15% 향상시켰다.
또한 신약 개발 과정에서도 AI가 활용되어, 기존 10년 이상 걸리던 신약 개발 기간을
절반으로 단축할 수 있을 것으로 기대된다. 다만 의료 AI의 윤리적 문제와
개인정보 보호에 대한 우려도 제기되고 있어, 관련 법규 정비가 시급한 상황이다.
"""

# 키워드 추출
print("=== 키워드 추출 ===")
response = ollama.chat(
    model="gemma3:1b",
    messages=[
        {"role": "system", "content": "주어진 텍스트에서 핵심 키워드 5개를 추출하세요. 키워드만 쉼표로 구분하여 나열하세요."},
        {"role": "user", "content": article}
    ]
)
print(response["message"]["content"])

# 요약
print("\n=== 3줄 요약 ===")
response = ollama.chat(
    model="gemma3:1b",
    messages=[
        {"role": "system", "content": "주어진 텍스트를 정확히 3줄로 요약하세요. 각 줄은 한 문장으로 작성하세요."},
        {"role": "user", "content": article}
    ]
)
print(response["message"]["content"])
