"""
5주차 실습 2: 다양한 Pipeline 태스크 체험
- 감성 분석 (한국어 지원)
- 제로샷 분류
- 한국어 → 영어 번역
"""

from transformers import pipeline
import torch

# GPU/CPU 자동 감지
device = 0 if torch.cuda.is_available() else -1

# ─── 1. 감성 분석 (한국어 지원) ───
print("=" * 60)
print("1. 다국어 감성 분석")
print("=" * 60)

classifier = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    device=device
)

texts = [
    "이 영화 정말 재미있었어요!",
    "서비스가 너무 불친절했습니다.",
    "가격 대비 괜찮았어요."
]

for text in texts:
    result = classifier(text)[0]
    stars = int(result['label'][0])
    print(f"  {'⭐' * stars} {result['label']:>10s} | \"{text}\"")

# ─── 2. 제로샷 분류 ───
print(f"\n{'=' * 60}")
print("2. 제로샷 분류")
print("=" * 60)

zero_clf = pipeline("zero-shot-classification", device=device)

news = "삼성전자가 새로운 AI 칩을 발표했습니다."
categories = ["technology", "sports", "politics", "entertainment"]

result = zero_clf(news, candidate_labels=categories)
print(f"  뉴스: \"{news}\"")
for label, score in zip(result['labels'], result['scores']):
    bar = "█" * int(score * 30)
    print(f"    {label:>15s}: {score:.4f} {bar}")

# ─── 3. 한국어 → 영어 번역 ───
print(f"\n{'=' * 60}")
print("3. 한국어 → 영어 번역")
print("=" * 60)

## transformers < 5.0.0
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-ko-en", device=device)

ko_texts = [
    "오늘 날씨가 정말 좋습니다.",
    "인공지능 수업이 재미있어요.",
    "빅데이터 분석 프로젝트를 진행하고 있습니다."
]

for text in ko_texts:
    result = translator(text)
    print(f"  한국어: {text}")
    print(f"  영  어: {result[0]['translation_text']}\n")

print("=" * 60)
print("모든 태스크 완료!")
print("=" * 60)
