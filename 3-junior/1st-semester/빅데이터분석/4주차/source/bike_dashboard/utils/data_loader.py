# utils/data_loader.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import re
from pathlib import Path


# ---- 로컬 캐시 경로 ----
# data_loader.py 기준으로 상위 폴더(bike_dashboard/)의 data/ 폴더에 저장
_DATA_DIR = Path(__file__).parent.parent / "data"
_LOCAL_CSV = _DATA_DIR / "bike_data.csv"

# ---- Google Drive 파일 다운로드 URL ----
# /file/d/{FILE_ID}/view 형식에서 FILE_ID를 추출하여 직접 다운로드 URL로 변환
GDRIVE_FILE_ID = "1ez3L8CfSuH0XHAnKuAoLknMgtl1vaXwC"
GDRIVE_URL = f"https://drive.google.com/uc?export=download&id={GDRIVE_FILE_ID}"

# 데이터 출처: 서울 열린데이터 광장 — 서울특별시 공공자전거 이용정보(월별)
# https://data.seoul.go.kr/dataList/OA-21229/F/1/datasetView.do


def _load_local_csv():
    """로컬에 저장된 CSV 파일을 읽어 DataFrame으로 반환합니다."""
    df = pd.read_csv(
        _LOCAL_CSV,
        encoding="utf-8-sig",
        on_bad_lines="skip"
    )
    return df


def _fetch_from_gdrive():
    """Google Drive에서 CSV 파일을 다운로드하고 로컬에 저장한 뒤 DataFrame으로 반환합니다."""
    session = requests.Session()
    resp = session.get(GDRIVE_URL, timeout=30, stream=True)

    # 대용량 파일은 바이러스 검사 경고 페이지가 뜰 수 있음 → 확인 토큰 필요
    if b"<!DOCTYPE html>" in resp.content[:100]:
        confirm_match = re.search(r'confirm=([0-9A-Za-z_-]+)', resp.text)
        uuid_match = re.search(r'uuid=([0-9A-Za-z_-]+)', resp.text)

        if confirm_match:
            url = f"{GDRIVE_URL}&confirm={confirm_match.group(1)}"
        elif uuid_match:
            url = f"{GDRIVE_URL}&confirm=t&uuid={uuid_match.group(1)}"
        else:
            url = f"{GDRIVE_URL}&confirm=t"

        resp = session.get(url, timeout=60)

    resp.raise_for_status()

    # EUC-KR → DataFrame으로 읽기
    df = pd.read_csv(
        io.BytesIO(resp.content),
        encoding="euc-kr",
        encoding_errors="replace",
        on_bad_lines="skip"
    )

    # 로컬에 UTF-8로 저장 (다음부터는 로컬에서 빠르게 읽기)
    _DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(_LOCAL_CSV, index=False, encoding="utf-8-sig")

    return df


def _generate_simulation_data():
    """네트워크 오류 시 사용할 시뮬레이션 데이터를 생성합니다."""
    np.random.seed(42)
    n = 5000

    stations = ['여의도역', '강남역', '홍대입구', '서울역', '잠실역',
                '신촌역', '합정역', '건대입구', '왕십리역', '이태원역']
    dates = pd.date_range('2025-01-01', periods=90)

    df = pd.DataFrame({
        '날짜': np.random.choice(dates, n),
        '대여소': np.random.choice(stations, n),
        '대여건수': np.random.poisson(lam=15, size=n),
        '반납건수': np.random.poisson(lam=14, size=n),
        '이용시간(분)': np.random.exponential(scale=25, size=n).astype(int) + 5
    })
    df['날짜'] = pd.to_datetime(df['날짜'])
    df = df.sort_values(['날짜', '대여소']).reset_index(drop=True)
    return df


def _transform_raw_data(df):
    """CSV 원본 데이터를 대시보드용 형식으로 변환합니다.

    원본 컬럼: 대여일자(YYYYMM), 대여소번호, 대여소명, 대여구분코드,
              성별, 연령대코드, 이용건수, 운동량, 탄소량, 이동거리(M), 이용시간(분)

    변환 후: 날짜, 대여소, 대여건수, 반납건수, 이용시간(분)
    """
    # 필수 컬럼 확인
    required = ["대여일자", "대여소명", "이용건수", "이용시간(분)"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"필수 컬럼 '{col}'이 데이터에 없습니다. 컬럼: {df.columns.tolist()}")

    # 대여일자(YYYYMM) → 날짜 (해당 월의 1일로 변환)
    df["날짜"] = pd.to_datetime(df["대여일자"].astype(str), format="%Y%m")

    # 대여소명에서 번호 제거 (예: "102. 망원역 1번출구 앞" → "망원역 1번출구 앞")
    df["대여소"] = df["대여소명"].str.replace(r"^\d+\.\s*", "", regex=True)

    # 숫자형 변환
    df["대여건수"] = pd.to_numeric(df["이용건수"], errors="coerce").fillna(0).astype(int)
    df["이용시간(분)"] = pd.to_numeric(df["이용시간(분)"], errors="coerce").fillna(0).astype(int)

    # 대여소별로 집계 (월별 + 대여소별 합산)
    result = df.groupby(["날짜", "대여소"]).agg(
        대여건수=("대여건수", "sum"),
        이용시간_총=("이용시간(분)", "sum"),
    ).reset_index()

    # 반납건수는 원본 데이터에 없으므로 대여건수 기반으로 추정
    np.random.seed(42)
    result["반납건수"] = (result["대여건수"] * np.random.uniform(0.90, 0.96, len(result))).astype(int)

    # 이용시간: 총합 → 건당 평균으로 변환
    result["이용시간(분)"] = (result["이용시간_총"] / result["대여건수"].replace(0, 1)).astype(int)
    result = result.drop(columns=["이용시간_총"])

    result = result.sort_values(["날짜", "대여소"]).reset_index(drop=True)
    return result


@st.cache_data(ttl="1h", show_spinner="데이터를 불러오는 중...")
def _load_bike_data_cached():
    """캐싱되는 데이터 로딩 함수 (내부용, UI 요소 호출 금지)"""

    # 1순위: 로컬 CSV (이전에 다운로드한 파일)
    if _LOCAL_CSV.exists():
        try:
            raw_df = _load_local_csv()
            df = _transform_raw_data(raw_df)
            return df, "local"
        except Exception:
            pass

    # 2순위: Google Drive CSV 다운로드 → 로컬에 저장
    try:
        raw_df = _fetch_from_gdrive()
        df = _transform_raw_data(raw_df)
        return df, "gdrive"
    except Exception:
        pass

    # 2순위: 시뮬레이션 데이터
    df = _generate_simulation_data()
    return df, "simulation"


def load_bike_data():
    """따릉이 이용 데이터 로딩 — Google Drive CSV 우선, 실패 시 시뮬레이션 데이터 사용"""
    df, source = _load_bike_data_cached()

    if source == "local":
        st.toast("✅ 로컬 CSV에서 데이터를 불러왔습니다.", icon="📂")
    elif source == "gdrive":
        st.toast("✅ Google Drive에서 다운로드 후 로컬에 저장했습니다.", icon="🌐")
    else:
        st.toast("📊 시뮬레이션 데이터를 사용합니다.", icon="🔄")

    return df


@st.cache_data(ttl="1h", show_spinner="원본 데이터를 불러오는 중...")
def _load_raw_data_cached():
    """원본 CSV 데이터를 집계 없이 그대로 반환합니다 (내부용)."""
    if _LOCAL_CSV.exists():
        try:
            return _load_local_csv(), "local"
        except Exception:
            pass
    try:
        return _fetch_from_gdrive(), "gdrive"
    except Exception:
        pass
    return pd.DataFrame(), "empty"


def load_raw_data():
    """원본 CSV 데이터를 집계 없이 그대로 반환합니다."""
    df, _ = _load_raw_data_cached()
    return df


@st.cache_data
def get_station_summary(df):
    """대여소별 요약 통계"""
    if df.empty:
        return pd.DataFrame()

    summary = df.groupby("대여소").agg(
        총대여건수=("대여건수", "sum"),
        총반납건수=("반납건수", "sum"),
        평균이용시간=("이용시간(분)", "mean"),
        일평균대여=("대여건수", lambda x: x.sum() / max(df["날짜"].nunique(), 1)),
    ).round(1).reset_index()
    return summary
