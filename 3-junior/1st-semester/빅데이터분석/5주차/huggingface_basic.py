"""
5주차 실습 1: HuggingFace Pipeline 기초
- 감성 분석(Sentiment Analysis) 파이프라인 사용
"""

from transformers import pipeline
import torch

# GPU/CPU 자동 감지
device = 0 if torch.cuda.is_available() else -1

# 1. 파이프라인 생성 (처음 실행 시 모델 다운로드)
print("모델 로딩 중...")
classifier = pipeline("sentiment-analysis", device=device)
print("모델 로딩 완료!\n")

# 2. 단일 문장 분석
text = "I really enjoyed this lecture!"
result = classifier(text)
print(f"입력: {text}")
print(f"결과: {result[0]['label']} (확신도: {result[0]['score']:.4f})")
print()

# 3. 여러 문장 분석
print("=" * 50)
print("여러 문장 감성 분석")
print("=" * 50)

sentences = [
    "Python is amazing!",
    "I don't like bugs in my code.",
    "The food was okay, nothing special.",
    "This is the best day ever!",
    "I'm so frustrated with this error."
]

results = classifier(sentences)

for sentence, res in zip(sentences, results):
    emoji = "😊" if res['label'] == 'POSITIVE' else "😞"
    score_bar = "█" * int(res['score'] * 20)
    print(f"{emoji} [{res['label']:>8}] {res['score']:.4f} {score_bar}")
    print(f"   \"{sentence}\"")
    print()

# 4. 직접 입력해보기
print("=" * 50)
print("직접 문장을 입력해서 테스트해보세요!")
print("(종료하려면 'quit' 입력)")
print("=" * 50)

while True:
    user_input = input("\n문장 입력: ")
    if user_input.lower() == 'quit':
        print("프로그램을 종료합니다.")
        break

    result = classifier(user_input)
    label = result[0]['label']
    score = result[0]['score']
    emoji = "😊" if label == 'POSITIVE' else "😞"
    print(f"  → {emoji} {label} (확신도: {score:.4f})")
