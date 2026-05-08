"""
실습 4-B: 공격 키워드 빈도 분석 (터미널 버전)
=============================================
1교시에서 배운 공격 키워드가 실제 CSIC 2010 데이터에
얼마나 나타나는지 확인합니다.

Streamlit 없이 터미널에서 바로 실행할 수 있는 버전입니다.
(Streamlit 대시보드 버전: streamlit run eda_visualization.py)

실행: python eda_keyword_analysis.py
"""

import pandas as pd
import os
import re
from urllib.parse import unquote

print("=" * 65)
print("  [실습 4-B] 공격 키워드 빈도 분석")
print("=" * 65)

# 데이터 로드
data_path = os.path.join(os.path.dirname(__file__), "csic2010_requests.csv")
if not os.path.exists(data_path):
    print(f"\n  !! csic2010_requests.csv 파일이 없습니다.")
    print(f"  >> 먼저 download_csic2010.py를 실행하세요.")
    exit()

df = pd.read_csv(data_path)
print(f"\n  데이터 로드: {len(df):,}건")

# URL 디코딩 + 결합 텍스트
df["url_decoded"] = df["url"].apply(lambda x: unquote(str(x), encoding="latin-1"))
df["body_decoded"] = df["body"].fillna("").apply(lambda x: unquote(str(x), encoding="latin-1"))
df["full_text"] = df["url_decoded"] + " " + df["body_decoded"]


# ============================================================
# 1. 공격 키워드 카테고리별 탐지
# ============================================================
print(f"\n{'─' * 65}")
print("  [1] 공격 키워드 카테고리별 빈도")
print(f"{'─' * 65}")

attack_categories = {
    "SQL Injection": ["'", "select", "union", "drop", "insert",
                      "delete", "update", "or '", "1=1", "--"],
    "XSS": ["<script", "alert(", "onerror", "<iframe",
            "<img", "javascript:", "onfocus"],
    "Path Traversal": ["../", "..\\", "/etc/passwd", "/etc/shadow"],
    "Command Injection": ["; ", "|", "&&", "/bin/", "cat ", "rm ", "wget"],
    "CRLF Injection": ["%0d", "%0a"],
}

print(f"\n  {'카테고리':<20s} | {'정상':>8s} | {'공격':>8s} | {'공격 집중도':>10s}")
print(f"  {'─' * 20}-+-{'─' * 8}-+-{'─' * 8}-+-{'─' * 10}")

normal_text = df[df["label"] == "Normal"]["full_text"]
attack_text = df[df["label"] == "Anomalous"]["full_text"]

for category, keywords in attack_categories.items():
    normal_count = 0
    attack_count = 0
    for kw in keywords:
        normal_count += normal_text.str.contains(re.escape(kw), case=False, na=False).sum()
        attack_count += attack_text.str.contains(re.escape(kw), case=False, na=False).sum()

    total = normal_count + attack_count
    concentration = attack_count / max(total, 1) * 100
    print(f"  {category:<20s} | {normal_count:>8,} | {attack_count:>8,} | {concentration:>9.1f}%")


# ============================================================
# 2. 개별 키워드 상세 분석
# ============================================================
print(f"\n{'─' * 65}")
print("  [2] 개별 키워드 상세 빈도 (공격에서 많이 발견된 순)")
print(f"{'─' * 65}")

results = []
for category, keywords in attack_categories.items():
    for kw in keywords:
        n_count = normal_text.str.contains(re.escape(kw), case=False, na=False).sum()
        a_count = attack_text.str.contains(re.escape(kw), case=False, na=False).sum()
        results.append({
            "category": category, "keyword": kw,
            "normal": n_count, "attack": a_count,
        })

result_df = pd.DataFrame(results).sort_values("attack", ascending=False)

print(f"\n  {'키워드':<15s} | {'카테고리':<20s} | {'정상':>6s} | {'공격':>6s}")
print(f"  {'─' * 15}-+-{'─' * 20}-+-{'─' * 6}-+-{'─' * 6}")

for _, row in result_df.head(20).iterrows():
    marker = " ★" if row["attack"] > row["normal"] * 2 else ""
    print(f"  {row['keyword']:<15s} | {row['category']:<20s} | "
          f"{row['normal']:>6,} | {row['attack']:>6,}{marker}")

print(f"\n  ★ = 공격에서 정상보다 2배 이상 많이 발견된 키워드")


# ============================================================
# 3. URL 인코딩 패턴 분석
# ============================================================
print(f"\n{'─' * 65}")
print("  [3] URL 인코딩 패턴 분석 (인코딩 전 원본 URL 기준)")
print(f"{'─' * 65}")

encoded_patterns = {
    "%27": "'  (작은따옴표 — SQL Injection)",
    "%3C": "<  (꺾쇠 — XSS)",
    "%3E": ">  (꺾쇠 닫기 — XSS)",
    "%2F": "/  (슬래시 — Path Traversal)",
    "%2E": ".  (점 — Path Traversal)",
    "%0D": "CR (캐리지리턴 — CRLF Injection)",
    "%0A": "LF (라인피드 — CRLF Injection)",
    "%20": "   (공백 — SQL 키워드 구분)",
    "%00": "NULL (널바이트 — 우회 시도)",
}

print(f"\n  {'패턴':<6s} | {'의미':<35s} | {'정상':>6s} | {'공격':>6s}")
print(f"  {'─' * 6}-+-{'─' * 35}-+-{'─' * 6}-+-{'─' * 6}")

# 인코딩 전 원본 URL에서 검색
normal_url = df[df["label"] == "Normal"]["url"]
attack_url = df[df["label"] == "Anomalous"]["url"]

for pattern, meaning in encoded_patterns.items():
    n_count = normal_url.str.contains(pattern, case=False, na=False).sum()
    a_count = attack_url.str.contains(pattern, case=False, na=False).sum()
    if n_count + a_count > 0:
        print(f"  {pattern:<6s} | {meaning:<35s} | {n_count:>6,} | {a_count:>6,}")


# ============================================================
# 4. 접근 경로(Path) 분석
# ============================================================
print(f"\n{'─' * 65}")
print("  [4] 가장 많이 접근된 경로 (정상 vs 공격)")
print(f"{'─' * 65}")

df["path"] = df["url_decoded"].str.split("?").str[0]

print(f"\n  === 정상 요청 Top 5 ===")
normal_paths = df[df["label"] == "Normal"]["path"].value_counts().head(5)
for path, count in normal_paths.items():
    print(f"    {path:<50s} {count:>6,}건")

print(f"\n  === 공격 요청 Top 5 ===")
attack_paths = df[df["label"] == "Anomalous"]["path"].value_counts().head(5)
for path, count in attack_paths.items():
    print(f"    {path:<50s} {count:>6,}건")


# ============================================================
# 5. URL 길이 비교
# ============================================================
print(f"\n{'─' * 65}")
print("  [5] URL 길이 비교 (정상 vs 공격)")
print(f"{'─' * 65}")

df["url_length"] = df["url_decoded"].str.len()

for label in ["Normal", "Anomalous"]:
    subset = df[df["label"] == label]["url_length"]
    print(f"\n  {label}:")
    print(f"    평균: {subset.mean():.0f},  중앙값: {subset.median():.0f},  "
          f"최대: {subset.max():,},  표준편차: {subset.std():.0f}")

print(f"\n  >> 공격 요청의 URL이 평균적으로 더 깁니다!")
print(f"     이 차이가 8주차 IQR 이상치 탐지의 근거가 됩니다.")


print(f"\n{'=' * 65}")
print("  키워드 분석 완료!")
print("  Streamlit 대시보드로 시각적 탐색: streamlit run eda_visualization.py")
print(f"{'=' * 65}")
