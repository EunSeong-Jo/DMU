import pandas as pd
import numpy as np
import time

# ──────────────────────────────────────
# 10만 행 테스트 데이터 생성
# ──────────────────────────────────────
N = 100_000
np.random.seed(42)

df = pd.DataFrame({
    "카테고리": np.random.choice(["컴퓨터", "주변기기", "소프트웨어", "네트워크", "보안"], N),
    "가격": np.random.randint(10000, 2000000, N),
    "판매량": np.random.randint(1, 500, N),
    "평점": np.random.uniform(1.0, 5.0, N).round(1)
})

print(f"테스트 데이터: {N:,}행 × {df.shape[1]}열")
print(f"메모리: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")

# ──────────────────────────────────────
# 테스트 1: 새 컬럼 생성 — for 루프 vs 벡터 연산
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("테스트 1: 할인가 계산 (가격 × 0.9)")
print("=" * 60)

# ❌ 느린 방법: for 루프
start = time.time()
for i in range(len(df)):
    df.loc[i, "할인가_slow"] = df.loc[i, "가격"] * 0.9
t_slow = time.time() - start
print(f"  ❌ for 루프:   {t_slow:.3f}초")

# ✅ 빠른 방법: 벡터 연산
start = time.time()
df["할인가_fast"] = df["가격"] * 0.9
t_fast = time.time() - start
print(f"  ✅ 벡터 연산:  {t_fast:.5f}초")
print(f"  → 벡터 연산이 {t_slow / t_fast:.0f}배 빠름!")

# ──────────────────────────────────────
# 테스트 2: 조건부 값 할당 — apply vs np.where
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("테스트 2: 등급 분류 (평점 >= 4.5 → '우수', 아니면 '보통')")
print("=" * 60)

# ❌ 느린 방법: apply + lambda
start = time.time()
df["등급_slow"] = df["평점"].apply(lambda x: "우수" if x >= 4.5 else "보통")
t_slow = time.time() - start
print(f"  ❌ apply:      {t_slow:.3f}초")

# ✅ 빠른 방법: np.where
start = time.time()
df["등급_fast"] = np.where(df["평점"] >= 4.5, "우수", "보통")
t_fast = time.time() - start
print(f"  ✅ np.where:   {t_fast:.5f}초")
print(f"  → np.where가 {t_slow / t_fast:.0f}배 빠름!")

# ──────────────────────────────────────
# 테스트 3: Category 타입 메모리 절약
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("테스트 3: Category 타입 변환 효과")
print("=" * 60)

mem_before = df["카테고리"].memory_usage(deep=True) / 1024
df["카테고리"] = df["카테고리"].astype("category")
mem_after = df["카테고리"].memory_usage(deep=True) / 1024

print(f"  변환 전 (object):   {mem_before:.1f} KB")
print(f"  변환 후 (category): {mem_after:.1f} KB")
print(f"  → {(1 - mem_after / mem_before) * 100:.0f}% 메모리 절약!")

# ──────────────────────────────────────
# 테스트 4: 다운캐스팅 효과
# ──────────────────────────────────────
print("\n" + "=" * 60)
print("테스트 4: 숫자 타입 다운캐스팅")
print("=" * 60)

mem_before = df[["가격", "판매량"]].memory_usage(deep=True).sum() / 1024
df["가격"] = df["가격"].astype("int32")
df["판매량"] = df["판매량"].astype("int16")
mem_after = df[["가격", "판매량"]].memory_usage(deep=True).sum() / 1024

print(f"  변환 전 (int64):    {mem_before:.1f} KB")
print(f"  변환 후 (int32/16): {mem_after:.1f} KB")
print(f"  → {(1 - mem_after / mem_before) * 100:.0f}% 메모리 절약!")

print("\n" + "=" * 60)
print("결론: 10만 행 이상에서는 벡터 연산 + 타입 최적화가 필수!")
print("=" * 60)
