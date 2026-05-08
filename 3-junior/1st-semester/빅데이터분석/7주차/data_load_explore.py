"""
실습 3: 데이터 로드 및 기본 탐색
================================
CSIC 2010 HTTP 데이터셋(csic2010_requests.csv)을 로드하고
HTTP 요청의 구조와 정상/공격 분포를 파악합니다.

실행: python data_load_explore.py
"""

import pandas as pd
import numpy as np
import os

# ============================================================
# 1. 데이터 로드
# ============================================================
print("=" * 65)
print("  [실습 3] CSIC 2010 HTTP 데이터 로드 및 기본 탐색")
print("=" * 65)

data_path = os.path.join(os.path.dirname(__file__), "csic2010_requests.csv")

if not os.path.exists(data_path):
    print(f"\n  !! csic2010_requests.csv 파일이 없습니다.")
    print(f"  >> 먼저 download_csic2010.py를 실행하세요.")
    exit()

df = pd.read_csv(data_path)

print(f"\n  데이터 로드 완료!")
print(f"  파일: {data_path}")
print(f"  크기: {df.shape[0]:,}행 x {df.shape[1]}열")


# ============================================================
# 2. 기본 정보 확인
# ============================================================
print(f"\n{'─' * 65}")
print("  [2] 데이터 기본 정보")
print(f"{'─' * 65}")

print(f"\n  전체 HTTP 요청 수: {len(df):,}건")
print(f"  컬럼 수: {df.shape[1]}개")
print(f"  메모리 사용량: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")


# ============================================================
# 3. 컬럼 목록 확인
# ============================================================
print(f"\n{'─' * 65}")
print("  [3] 컬럼 목록")
print(f"{'─' * 65}")

for i, col in enumerate(df.columns, 1):
    dtype = str(df[col].dtype)
    non_null = df[col].notna().sum()
    print(f"  {i:3d}. {col:20s}  ({dtype:8s}) — 값 있는 행: {non_null:,}")


# ============================================================
# 4. 라벨(Label) 분포 확인 ★★★
# ============================================================
print(f"\n{'─' * 65}")
print("  [4] 라벨 분포 (Normal vs Anomalous) ★")
print(f"{'─' * 65}")

label_counts = df["label"].value_counts()
label_ratio = df["label"].value_counts(normalize=True) * 100

print(f"\n  {'라벨':<15s} | {'건수':>8s} | {'비율':>6s} | 시각화")
print(f"  {'─' * 15}-+-{'─' * 8}-+-{'─' * 6}-+-{'─' * 30}")

for label in label_counts.index:
    count = label_counts[label]
    ratio = label_ratio[label]
    bar = "█" * int(ratio / 2)
    print(f"  {label:<15s} | {count:>8,} | {ratio:>5.1f}% | {bar}")

print(f"\n  >> 정상({label_counts.get('Normal', 0):,}건) vs "
      f"공격({label_counts.get('Anomalous', 0):,}건)")


# ============================================================
# 5. HTTP 메서드 분포
# ============================================================
print(f"\n{'─' * 65}")
print("  [5] HTTP 메서드 분포")
print(f"{'─' * 65}")

method_counts = df["method"].value_counts()
for method, count in method_counts.items():
    pct = count / len(df) * 100
    bar = "█" * int(pct / 2)
    print(f"  {method:6s}: {count:>8,}건 ({pct:5.1f}%) {bar}")


# ============================================================
# 6. 메서드별 정상/공격 교차 분석
# ============================================================
print(f"\n{'─' * 65}")
print("  [6] 메서드별 정상/공격 분포")
print(f"{'─' * 65}")

cross = pd.crosstab(df["method"], df["label"])
print(f"\n{cross.to_string()}")

# 공격 비율이 높은 메서드 확인
for method in cross.index:
    total = cross.loc[method].sum()
    anomalous = cross.loc[method].get("Anomalous", 0)
    ratio = anomalous / total * 100 if total > 0 else 0
    print(f"\n  {method}: 공격 비율 {ratio:.1f}%", end="")
    if ratio > 30:
        print(" ← 공격 비율 높음!", end="")
print()


# ============================================================
# 7. 실제 HTTP 요청 확인 ★★★
# ============================================================
print(f"\n{'─' * 65}")
print("  [7] 실제 HTTP 요청 샘플 확인 ★")
print(f"{'─' * 65}")

# 정상 요청 1건
print(f"\n  ═══ 정상 요청 (Normal) ═══")
normal = df[df["label"] == "Normal"].iloc[0]
print(f"  메서드: {normal['method']}")
print(f"  URL:    {normal['url'][:100]}{'...' if len(str(normal['url'])) > 100 else ''}")
print(f"  쿠키:   {str(normal['cookie'])[:60]}{'...' if len(str(normal['cookie'])) > 60 else ''}")
body = str(normal["body"]) if pd.notna(normal["body"]) and normal["body"] else "(없음)"
print(f"  본문:   {body[:100]}")

# 공격 요청 3건
print(f"\n  ═══ 공격 요청 (Anomalous) — 3건 ═══")
anomalous = df[df["label"] == "Anomalous"].sample(3, random_state=42)
for i, (_, row) in enumerate(anomalous.iterrows(), 1):
    print(f"\n  --- 공격 #{i} ---")
    print(f"  메서드: {row['method']}")
    url_display = str(row["url"])[:120]
    print(f"  URL:    {url_display}{'...' if len(str(row['url'])) > 120 else ''}")
    body = str(row["body"]) if pd.notna(row["body"]) and row["body"] else "(없음)"
    print(f"  본문:   {body[:120]}{'...' if len(body) > 120 else ''}")
    print(f"  → 1교시에서 배운 공격 패턴을 찾아보세요!")


# ============================================================
# 8. URL 길이 기본 통계
# ============================================================
print(f"\n{'─' * 65}")
print("  [8] URL 길이 기본 통계")
print(f"{'─' * 65}")

df["url_length"] = df["url"].str.len()

print(f"\n  {'구분':<12s} | {'평균':>8s} | {'중앙값':>8s} | {'최대':>8s}")
print(f"  {'─' * 12}-+-{'─' * 8}-+-{'─' * 8}-+-{'─' * 8}")

for label in ["Normal", "Anomalous"]:
    subset = df[df["label"] == label]["url_length"]
    print(f"  {label:<12s} | {subset.mean():>8.0f} | {subset.median():>8.0f} | {subset.max():>8,}")

print(f"\n  >> 공격 요청의 URL이 평균적으로 더 깁니다! (공격 코드가 삽입되므로)")


# ============================================================
# 9. 데이터 품질 확인
# ============================================================
print(f"\n{'─' * 65}")
print("  [9] 데이터 품질 확인")
print(f"{'─' * 65}")

# 결측치 확인
missing = df.isnull().sum()
missing_cols = missing[missing > 0]
print(f"\n  결측치가 있는 컬럼:")
if len(missing_cols) > 0:
    for col, cnt in missing_cols.items():
        print(f"    - {col}: {cnt:,}건")
else:
    print("    없음 (body, cookie 등은 빈 문자열)")

# 빈 body (GET 요청)
empty_body = df["body"].fillna("").eq("").sum()
print(f"\n  본문(body)이 비어있는 요청: {empty_body:,}건 (대부분 GET 요청)")

print(f"\n{'=' * 65}")
print("  실습 3 완료! 다음: streamlit run eda_visualization.py")
print(f"{'=' * 65}")
