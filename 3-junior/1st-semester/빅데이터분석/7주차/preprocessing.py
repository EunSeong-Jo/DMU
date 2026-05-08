"""
실습 5: 데이터 전처리 + 특성 추출
=================================
HTTP 요청 텍스트에서 URL 디코딩, 텍스트 정리를 수행하고,
분류에 유용한 숫자형 특성(Feature)을 추출합니다.

실행: python preprocessing.py
"""

import pandas as pd
import numpy as np
import os
import re
import math
from urllib.parse import unquote, urlparse, parse_qs

print("=" * 65)
print("  [실습 5] 데이터 전처리 + 특성 추출")
print("=" * 65)

# 데이터 로드
data_path = os.path.join(os.path.dirname(__file__), "csic2010_requests.csv")
if not os.path.exists(data_path):
    print(f"\n  !! csic2010_requests.csv 파일이 없습니다.")
    print(f"  >> 먼저 download_csic2010.py를 실행하세요.")
    exit()

df = pd.read_csv(data_path)
print(f"\n  원본 데이터: {df.shape[0]:,}행 x {df.shape[1]}열")


# ============================================================
# Step 1: URL 디코딩
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 1: URL 디코딩 (인코딩된 문자 → 원래 문자)")
print(f"{'─' * 65}")

df["url_decoded"] = df["url"].apply(
    lambda x: unquote(str(x), encoding="latin-1")
)
df["body_decoded"] = df["body"].fillna("").apply(
    lambda x: unquote(str(x), encoding="latin-1")
)

# 디코딩 전후 비교 예시
sample = df[df["url"].str.contains("%27|%3C|%2e", case=False, na=False)]
if len(sample) > 0:
    row = sample.iloc[0]
    print(f"\n  디코딩 전: {str(row['url'])[:80]}...")
    print(f"  디코딩 후: {str(row['url_decoded'])[:80]}...")
else:
    print(f"\n  디코딩 적용 완료")

# URL + Body 결합 텍스트
df["full_text"] = df["url_decoded"] + " " + df["body_decoded"]
print(f"\n  >> URL과 Body를 결합한 분석용 텍스트(full_text) 생성 완료")


# ============================================================
# Step 2: 중복 확인
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 2: 중복 확인")
print(f"{'─' * 65}")

dup_count = df.duplicated(subset=["method", "url", "body"]).sum()
print(f"\n  중복 요청: {dup_count:,}건")
if dup_count > 0:
    print(f"  >> 학습용으로 중복은 유지합니다 (동일 요청 패턴도 의미 있음)")


# ============================================================
# Step 3: 기본 길이 특성 추출
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 3: 기본 길이 특성 추출")
print(f"{'─' * 65}")

df["url_length"] = df["url_decoded"].str.len()
df["body_length"] = df["body_decoded"].str.len()
df["total_length"] = df["url_length"] + df["body_length"]

print(f"\n  {'특성':<15s} | {'정상 평균':>10s} | {'공격 평균':>10s} | {'차이':>8s}")
print(f"  {'─' * 15}-+-{'─' * 10}-+-{'─' * 10}-+-{'─' * 8}")

for feat in ["url_length", "body_length", "total_length"]:
    normal_mean = df[df["label"] == "Normal"][feat].mean()
    attack_mean = df[df["label"] == "Anomalous"][feat].mean()
    diff = attack_mean - normal_mean
    sign = "+" if diff > 0 else ""
    print(f"  {feat:<15s} | {normal_mean:>10.1f} | {attack_mean:>10.1f} | {sign}{diff:>7.1f}")


# ============================================================
# Step 4: URL 구조 특성 추출
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 4: URL 구조 특성 추출")
print(f"{'─' * 65}")


def extract_url_structure(url):
    """URL에서 구조적 특성 추출"""
    try:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        return {
            "num_params": len(params),
            "path_depth": parsed.path.count("/"),
            "has_query": 1 if parsed.query else 0,
            "query_length": len(parsed.query),
        }
    except Exception:
        return {"num_params": 0, "path_depth": 0, "has_query": 0, "query_length": 0}


url_features = df["url_decoded"].apply(extract_url_structure).apply(pd.Series)
df = pd.concat([df, url_features], axis=1)

# POST body에서도 파라미터 수 추출
df["body_num_params"] = df["body_decoded"].apply(
    lambda x: len(x.split("&")) if x and "=" in x else 0
)

print(f"\n  추출된 URL 구조 특성: num_params, path_depth, has_query, query_length, body_num_params")
print(f"  >> 공격 요청의 파라미터 수 평균: {df[df['label']=='Anomalous']['num_params'].mean():.1f}")
print(f"  >> 정상 요청의 파라미터 수 평균: {df[df['label']=='Normal']['num_params'].mean():.1f}")


# ============================================================
# Step 5: 공격 키워드 탐지 특성 추출 ★★
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 5: 공격 키워드 탐지 특성 추출 ★")
print(f"{'─' * 65}")


def extract_attack_features(text):
    """텍스트에서 공격 관련 특성 추출"""
    text_lower = text.lower()

    # SQL Injection
    sql_keywords = ["select", "union", "drop", "insert", "delete",
                    "update", "' or", "1=1", "1'='1", "--", "/*"]
    has_sql = int(any(kw in text_lower for kw in sql_keywords))
    sql_count = sum(1 for kw in sql_keywords if kw in text_lower)

    # XSS
    xss_keywords = ["<script", "alert(", "onerror", "<iframe",
                    "<img", "javascript:", "onfocus", "onload"]
    has_xss = int(any(kw in text_lower for kw in xss_keywords))

    # Path Traversal
    has_traversal = int("../" in text or "..\\" in text)
    traversal_count = text.count("../") + text.count("..\\")

    # Command Injection ('|'는 정상 요청에도 나타날 수 있어 오탐 가능)
    cmd_patterns = ["; ", "| ", "&&", "/bin/", "/etc/", "exec"]
    has_cmd = int(any(p in text_lower for p in cmd_patterns))

    # CRLF Injection
    has_crlf = int("%0d" in text_lower or "%0a" in text_lower)

    # 특수문자 개수 및 비율
    num_special = len(re.findall(r"['\";|<>&`\\]", text))
    special_ratio = num_special / max(len(text), 1)

    # 숫자 점(dot) 슬래시 개수
    num_dots = text.count(".")
    num_slashes = text.count("/")

    # 공백 개수 (SQL Injection은 키워드 사이에 공백이 많음)
    num_spaces = text.count(" ") + text.count("%20") + text.count("+")

    return {
        "has_sql": has_sql, "sql_keyword_count": sql_count,
        "has_xss": has_xss, "has_traversal": has_traversal,
        "traversal_count": traversal_count,
        "has_cmd_injection": has_cmd, "has_crlf": has_crlf,
        "num_special_chars": num_special, "special_char_ratio": special_ratio,
        "num_dots": num_dots, "num_slashes": num_slashes,
        "num_spaces": num_spaces,
    }


print("\n  키워드 특성 추출 중...")
attack_features = df["full_text"].apply(extract_attack_features).apply(pd.Series)
df = pd.concat([df, attack_features], axis=1)

# 키워드 특성 요약
keyword_features = ["has_sql", "has_xss", "has_traversal", "has_cmd_injection", "has_crlf"]
print(f"\n  {'특성':<20s} | {'정상':>6s} | {'공격':>6s} | 의미")
print(f"  {'─' * 20}-+-{'─' * 6}-+-{'─' * 6}-+-{'─' * 25}")

for feat in keyword_features:
    normal_sum = df[df["label"] == "Normal"][feat].sum()
    attack_sum = df[df["label"] == "Anomalous"][feat].sum()
    print(f"  {feat:<20s} | {normal_sum:>6,} | {attack_sum:>6,} | "
          f"{'공격에 집중!' if attack_sum > normal_sum * 2 else '양쪽 모두 존재'}")


# ============================================================
# Step 6: 통계적 특성 추출
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 6: 통계적 특성 추출 (엔트로피, 비율)")
print(f"{'─' * 65}")


def calculate_entropy(text):
    """섀넌 엔트로피 계산"""
    if not text:
        return 0.0
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    length = len(text)
    return -sum((c / length) * math.log2(c / length) for c in freq.values())


print("\n  엔트로피 계산 중...")
df["url_entropy"] = df["url_decoded"].apply(calculate_entropy)

df["digit_ratio"] = df["full_text"].apply(
    lambda x: sum(c.isdigit() for c in x) / max(len(x), 1)
)
df["upper_ratio"] = df["full_text"].apply(
    lambda x: sum(c.isupper() for c in x) / max(len(x), 1)
)

print(f"\n  정상 URL 엔트로피 평균: {df[df['label']=='Normal']['url_entropy'].mean():.3f}")
print(f"  공격 URL 엔트로피 평균: {df[df['label']=='Anomalous']['url_entropy'].mean():.3f}")
print(f"  >> 공격 요청은 특수문자가 많아 엔트로피가 다른 경향이 있습니다")


# ============================================================
# Step 7: 전처리 결과 저장
# ============================================================
print(f"\n{'─' * 65}")
print("  Step 7: 전처리 결과 저장")
print(f"{'─' * 65}")

output_path = os.path.join(os.path.dirname(__file__), "csic2010_cleaned.csv")
df.to_csv(output_path, index=False, encoding="utf-8-sig")

# 추출된 특성 목록 출력
feature_cols = [
    "url_length", "body_length", "total_length",
    "num_params", "path_depth", "has_query", "query_length", "body_num_params",
    "has_sql", "sql_keyword_count", "has_xss",
    "has_traversal", "traversal_count",
    "has_cmd_injection", "has_crlf",
    "num_special_chars", "special_char_ratio",
    "num_dots", "num_slashes", "num_spaces",
    "url_entropy", "digit_ratio", "upper_ratio",
]

print(f"\n  저장 완료: csic2010_cleaned.csv")
print(f"  최종 데이터: {df.shape[0]:,}행 x {df.shape[1]}열")
print(f"\n  추출된 숫자형 특성 ({len(feature_cols)}개):")
for i, col in enumerate(feature_cols, 1):
    print(f"    {i:2d}. {col}")

print(f"\n{'=' * 65}")
print("  전처리 + 특성 추출 완료! 다음: python feature_engineering.py")
print(f"{'=' * 65}")
