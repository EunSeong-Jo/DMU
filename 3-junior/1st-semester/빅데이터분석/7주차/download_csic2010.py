"""
CSIC 2010 HTTP 데이터셋 준비 (Kaggle CSV → 수업용 CSV)
====================================================
Kaggle에서 다운받은 csic_database.csv를 읽어 컬럼을 표준화하고
수업용 CSV(csic2010_requests.csv)를 생성합니다.

원본 출처:
  https://www.kaggle.com/datasets/ispangler/csic-2010-web-application-attacks

============================================================
  사용 방법
============================================================

  [기본] 1만 건만 샘플링 (수업용 — 권장)
    python download_csic2010.py

  [전체] 원본 61,065건 모두 사용
    python download_csic2010.py --full

============================================================
  사전 조건
============================================================
  Kaggle CSV가 아래 경로에 있어야 합니다:
    data/archive/csic_database.csv

실행 결과: csic2010_requests.csv (이 스크립트와 같은 폴더)
"""

import os
import re
import sys
import argparse
import pandas as pd


SAMPLE_SIZE_DEFAULT = 10_000
RANDOM_SEED = 42

# Kaggle CSV의 원본 URL은 'http://localhost:8080/path?q HTTP/1.1' 형식
URL_PREFIX_RE = re.compile(r"^https?://[^/]+", re.IGNORECASE)
URL_SUFFIX_RE = re.compile(r"\s+HTTP/[\d.]+\s*$", re.IGNORECASE)


def normalize_url(raw_url):
    """'http://localhost:8080/path?q HTTP/1.1' → '/path?q' 와 'HTTP/1.1' 분리"""
    if pd.isna(raw_url):
        return "", ""
    s = str(raw_url).strip()
    # HTTP 버전 추출
    m = URL_SUFFIX_RE.search(s)
    http_version = m.group(0).strip() if m else "HTTP/1.1"
    s = URL_SUFFIX_RE.sub("", s)
    # 호스트 접두어 제거
    s = URL_PREFIX_RE.sub("", s)
    return s.strip(), http_version


def main():
    parser = argparse.ArgumentParser(description="Kaggle CSIC 2010 → 수업용 CSV")
    parser.add_argument(
        "--full", action="store_true",
        help="원본 전체(약 61,000건) 사용. 미지정 시 1만 건만 샘플링"
    )
    parser.add_argument(
        "--src", default=None,
        help="Kaggle csic_database.csv 경로 (기본: data/archive/csic_database.csv)"
    )
    args = parser.parse_args()

    print("=" * 65)
    print("  CSIC 2010 (Kaggle) → 수업용 CSV 변환")
    print("=" * 65)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    src = args.src or os.path.join(script_dir, "data", "archive", "csic_database.csv")

    if not os.path.exists(src):
        print(f"\n  !! 원본 파일을 찾을 수 없습니다:")
        print(f"     {src}")
        print(f"\n  Kaggle에서 다운로드 후 위 경로에 저장하세요:")
        print(f"  https://www.kaggle.com/datasets/ispangler/csic-2010-web-application-attacks")
        sys.exit(1)

    print(f"\n  원본 로드: {src}")
    raw = pd.read_csv(src)
    print(f"  원본 크기: {len(raw):,}건 x {raw.shape[1]}열")

    # 컬럼 정규화
    df = pd.DataFrame()
    df["label"] = raw.iloc[:, 0]                         # Unnamed: 0 → label
    df["method"] = raw["Method"]
    url_split = raw["URL"].apply(normalize_url)
    df["url"] = url_split.apply(lambda x: x[0])
    df["http_version"] = url_split.apply(lambda x: x[1])
    df["host"] = raw["host"]
    df["user_agent"] = raw["User-Agent"]
    df["pragma"] = raw["Pragma"]
    df["cache_control"] = raw["Cache-Control"]
    df["accept"] = raw["Accept"]
    df["accept_encoding"] = raw["Accept-encoding"]
    df["accept_charset"] = raw["Accept-charset"]
    df["language"] = raw["language"]
    df["cookie"] = raw["cookie"]
    df["content_type"] = raw["content-type"]
    df["content_length"] = raw["lenght"]                 # 원본 오타 그대로
    df["connection"] = raw["connection"]
    df["body"] = raw["content"]
    df["classification"] = raw["classification"]         # 0=Normal, 1=Anomalous

    # 샘플링 (수업용 1만 건, 라벨 비율 유지)
    if not args.full:
        size = min(SAMPLE_SIZE_DEFAULT, len(df))
        normal_ratio = (df["label"] == "Normal").mean()
        n_normal = int(size * normal_ratio)
        n_anom = size - n_normal

        normal_df = df[df["label"] == "Normal"].sample(
            n=n_normal, random_state=RANDOM_SEED
        )
        anom_df = df[df["label"] == "Anomalous"].sample(
            n=n_anom, random_state=RANDOM_SEED
        )
        df = pd.concat([normal_df, anom_df]).sample(
            frac=1, random_state=RANDOM_SEED
        ).reset_index(drop=True)
        print(f"  샘플링: {size:,}건 (정상 {n_normal:,} + 공격 {n_anom:,})")
    else:
        print(f"  전체 사용: {len(df):,}건")

    # 라벨/메서드 분포
    print(f"\n  라벨 분포:")
    for label, count in df["label"].value_counts().items():
        pct = count / len(df) * 100
        bar = "█" * int(pct / 2)
        print(f"    {label:12s}: {count:>8,}건 ({pct:5.1f}%) {bar}")

    print(f"\n  HTTP 메서드 분포:")
    for method, count in df["method"].value_counts().items():
        print(f"    {method:6s}: {count:>8,}건")

    # 저장
    output_path = os.path.join(script_dir, "csic2010_requests.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    file_size = os.path.getsize(output_path) / 1024 / 1024
    print(f"\n{'=' * 65}")
    print(f"  저장 완료: csic2010_requests.csv")
    print(f"  크기: {len(df):,}건 x {df.shape[1]}열  ({file_size:.1f} MB)")
    print(f"{'=' * 65}")
    print(f"\n  >> 다음 단계: jupyter lab → data_load_explore.ipynb 열기")


if __name__ == "__main__":
    main()
