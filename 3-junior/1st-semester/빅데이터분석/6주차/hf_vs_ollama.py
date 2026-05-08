import ollama
from transformers import pipeline
import time

# ※ 영어 텍스트를 사용하는 이유: HuggingFace의 distilbert 감성 분석 모델이
#   영어 전용 모델이기 때문. Ollama의 gemma3는 영어/한국어 모두 가능.
text = "This movie was absolutely fantastic! The acting was superb."

# --- HuggingFace Pipeline ---
print("=== HuggingFace Pipeline ===")
start = time.time()
classifier = pipeline("sentiment-analysis",
                       model="distilbert-base-uncased-finetuned-sst-2-english")
result = classifier(text)
hf_time = time.time() - start
print(f"결과: {result}")
print(f"소요 시간: {hf_time:.2f}초")

# --- Ollama LLM ---
print("\n=== Ollama LLM ===")
start = time.time()
response = ollama.chat(
    model="gemma3:4b",
    messages=[
        {
            "role": "system",
            "content": '감성을 분석하여 {"label": "POSITIVE/NEGATIVE", "score": 0.0~1.0} JSON으로만 답하세요.'
        },
        {"role": "user", "content": text}
    ]
)
ollama_time = time.time() - start
print(f"결과: {response['message']['content']}")
print(f"소요 시간: {ollama_time:.2f}초")

print(f"\n--- 비교 ---")
print(f"HuggingFace: 구조화된 출력, {hf_time:.2f}초")
print(f"Ollama:      자연어/JSON 출력, {ollama_time:.2f}초")
