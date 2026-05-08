"""
5주차 2교시: 한국어 감성 분석 — 모델 비교
- 다국어 모델 vs 한국어 전용 모델 성능 비교
"""

from transformers import pipeline
import torch

# GPU/CPU 자동 감지
device = 0 if torch.cuda.is_available() else -1

# ── 모델 1: 다국어 모델 (별점 1~5) ──
multi_clf = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    device=device
)

# ── 모델 2: 한국어 감성 분석 전용 ──
ko_clf = pipeline(
    "sentiment-analysis",
    model="matthewburke/korean_sentiment",
    device=device
)

texts = [
    "이 제품 정말 좋아요! 강력 추천합니다.",
    "배송이 너무 늦고 포장도 엉망이었어요.",
    "가격은 괜찮은데 품질이 아쉬워요.",
]

print("=" * 60)
print("다국어 모델 vs 한국어 전용 모델 비교")
print("=" * 60)

for text in texts:
    r1 = multi_clf(text)[0]
    r2 = ko_clf(text)[0]
    print(f"\n입력: \"{text}\"")
    print(f"  다국어 모델: {r1['label']:>10s} ({r1['score']:.4f})")
    print(f"  한국어 전용: {r2['label']:>10s} ({r2['score']:.4f})")
