"""
5주차 2교시: 한국어 번역
- 한국어 → 영어
- 영어 → 한국어
"""

from transformers import pipeline
import torch

# GPU/CPU 자동 감지
device = 0 if torch.cuda.is_available() else -1

# 한국어 → 영어 번역
ko_to_en = pipeline("translation", model="Helsinki-NLP/opus-mt-ko-en", device=device)
result = ko_to_en("오늘 날씨가 정말 좋습니다.")
print("한→영:", result[0]['translation_text'])

# 영어 → 한국어 번역
en_to_ko = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ko", device=device)
result = en_to_ko("I love learning artificial intelligence!")
print("영→한:", result[0]['translation_text'])
