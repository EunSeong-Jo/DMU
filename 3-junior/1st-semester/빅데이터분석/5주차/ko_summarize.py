import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

# ── 1단계: Tokenizer + Model 직접 로드 ──
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = PreTrainedTokenizerFast.from_pretrained("gogamza/kobart-summarization")
model = BartForConditionalGeneration.from_pretrained("gogamza/kobart-summarization").to(device)

article = """
인공지능(AI) 기술이 다양한 산업에 빠르게 확산되고 있다. 의료 분야에서는 AI를 활용한
질병 진단 시스템이 의사의 판단을 보조하고 있으며, 금융 분야에서는 이상 거래 탐지와
신용 평가에 AI가 도입되었다. 교육 분야에서도 개인 맞춤형 학습 시스템이 등장하여
학생들의 학습 효율을 높이고 있다. 전문가들은 앞으로 AI가 더 많은 직업에 영향을
미칠 것으로 전망하면서도, 윤리적 문제와 일자리 변화에 대한 사회적 논의가 필요하다고
강조하고 있다.
"""

# ── 2단계: 토큰화 (텍스트 → 숫자) ──
inputs = tokenizer([article], return_tensors="pt", max_length=1024, truncation=True).to(device)

# ── 3단계: 모델 추론 (요약 생성) ──
summary_ids = model.generate(inputs["input_ids"], max_length=80, min_length=20, num_beams=4)

# ── 4단계: 후처리 (숫자 → 텍스트) ──
result = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
print("요약 결과:", result)
