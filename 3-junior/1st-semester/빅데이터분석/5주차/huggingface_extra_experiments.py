"""
5주차 추가 실험: Pipeline 다양한 입력 테스트
- 빨리 끝난 학생을 위한 추가 실험 코드
- 긴 문장, 빈 문자열, 숫자, 이중 부정, 풍자 등을 테스트
"""

from transformers import pipeline
import torch

# GPU/CPU 자동 감지
device = 0 if torch.cuda.is_available() else -1

# 파이프라인 생성
print("모델 로딩 중...")
classifier = pipeline("sentiment-analysis", device=device)
print("모델 로딩 완료!\n")


# ── 추가 실험 1: 긴 문장도 분석 가능한가? ──
print("=" * 60)
print("실험 1: 긴 문장 분석")
print("=" * 60)

long_text = (
    "Despite some minor flaws in the beginning, the movie gradually "
    "became more interesting and by the end I was completely captivated "
    "by the story."
)
result = classifier(long_text)
print(f"입력: {long_text}")
print(f"결과: {result[0]['label']} ({result[0]['score']:.4f})")
print("→ 전체 문맥을 고려하여 판단합니다\n")


# ── 추가 실험 2: 빈 문자열은? ──
print("=" * 60)
print("실험 2: 빈 문자열")
print("=" * 60)

try:
    result = classifier("")
    print(f"결과: {result[0]['label']} ({result[0]['score']:.4f})")
except Exception as e:
    print(f"에러 발생: {e}")
print("→ 빈 문자열은 에러가 발생하거나 의미 없는 결과가 나옵니다\n")


# ── 추가 실험 3: 숫자만 넣으면? ──
print("=" * 60)
print("실험 3: 숫자만 입력")
print("=" * 60)

result = classifier("12345")
print(f"입력: '12345'")
print(f"결과: {result[0]['label']} ({result[0]['score']:.4f})")
print("→ 의미 없는 입력에는 신뢰할 수 없는 결과가 나옵니다\n")


# ── 추가 실험 4: 애매한 문장과 이중 부정 ──
print("=" * 60)
print("실험 4: 애매한 문장 & 이중 부정")
print("=" * 60)

tricky_sentences = [
    "It was not bad.",                          # 이중 부정 (긍정 의미)
    "I can't say I didn't like it.",            # 삼중 부정 (긍정 의미)
    "The movie was okay.",                      # 중립적 표현
    "I suppose it could have been worse.",      # 소극적 긍정
]

results = classifier(tricky_sentences)
for sentence, res in zip(tricky_sentences, results):
    print(f"  입력: \"{sentence}\"")
    print(f"  결과: {res['label']} ({res['score']:.4f})")
    print()


# ── 추가 실험 5: 풍자 / 비꼬기 ──
print("=" * 60)
print("실험 5: 풍자 & 비꼬기 (Sarcasm)")
print("=" * 60)

sarcasm_sentences = [
    "Oh great, another bug in my code.",        # 풍자 (실제로는 부정)
    "Wow, what a wonderful day to debug.",      # 풍자 (실제로는 부정)
    "Sure, I just love working overtime.",       # 풍자 (실제로는 부정)
    "Thanks for nothing.",                       # 비꼬기
]

results = classifier(sarcasm_sentences)
for sentence, res in zip(sarcasm_sentences, results):
    print(f"  입력: \"{sentence}\"")
    print(f"  결과: {res['label']} ({res['score']:.4f})")
    print()

print("→ AI 모델은 풍자(sarcasm)를 잘 이해하지 못할 수 있습니다!")
print("  표면적으로 긍정 단어('great', 'wonderful', 'love')가 있으면")
print("  POSITIVE로 판단하는 경향이 있습니다.\n")


# ── 추가 실험 6: 한국어 문장 (영어 전용 모델) ──
print("=" * 60)
print("실험 6: 한국어 문장 (영어 전용 모델에 입력)")
print("=" * 60)

korean_sentences = [
    "나는 이 수업이 정말 좋아요!",
    "오늘 기분이 너무 안 좋다.",
    "파이썬은 재미있는 언어입니다.",
]

results = classifier(korean_sentences)
for sentence, res in zip(korean_sentences, results):
    print(f"  입력: \"{sentence}\"")
    print(f"  결과: {res['label']} ({res['score']:.4f})")
    print()

print("→ 이 모델은 영어 전용이므로 한국어 결과는 부정확합니다!")
print("  2교시에서 한국어 모델을 사용하는 방법을 배웁니다.")
