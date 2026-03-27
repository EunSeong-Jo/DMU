"""
전체 데이터 수집 통합 실행 스크립트
"""

from collect_apartment_data import ApartmentDataCollector
from collect_subway_data import SubwayDataCollector
from collect_bus_data import BusStopCollector
from collect_air_quality_data import AirQualityCollector
from collect_school_data import SchoolDataCollector

import os
from datetime import datetime

# ========================================
# API 키 설정
# ========================================
# 공공데이터포털에서 각각 발급받아 입력하세요

API_KEYS = {
    'MOLIT': 'YOUR_MOLIT_API_KEY',          # 국토교통부 (아파트 실거래가)
    'SEOUL': 'YOUR_SEOUL_API_KEY',          # 서울시 (지하철, 버스)
    'AIR_KOREA': 'YOUR_AIR_KOREA_API_KEY',  # 에어코리아 (대기질)
    'SCHOOL': 'YOUR_SCHOOL_API_KEY'         # 학교알리미 (학교 정보)
}

# ========================================
# 설정
# ========================================
SAVE_PATH = '../data/raw'
START_YEAR = 2020
END_YEAR = 2024

# ========================================
# 데이터 수집 함수
# ========================================

def collect_apartment_data():
    """아파트 실거래가 데이터 수집"""
    print("\n" + "=" * 70)
    print("1. 아파트 실거래가 데이터 수집")
    print("=" * 70)

    collector = ApartmentDataCollector(api_key=API_KEYS['MOLIT'])
    collector.collect_all(
        start_year=START_YEAR,
        end_year=END_YEAR,
        save_path=SAVE_PATH
    )

def collect_subway_data():
    """지하철역 데이터 수집"""
    print("\n" + "=" * 70)
    print("2. 지하철역 데이터 수집")
    print("=" * 70)

    collector = SubwayDataCollector(api_key=API_KEYS['SEOUL'])
    df = collector.fetch_subway_stations()

    if not df.empty:
        collector.save_data(df, save_path=SAVE_PATH)

def collect_bus_data():
    """버스정류장 데이터 수집"""
    print("\n" + "=" * 70)
    print("3. 버스정류장 데이터 수집")
    print("=" * 70)

    collector = BusStopCollector(api_key=API_KEYS['SEOUL'])
    df = collector.fetch_bus_stops()

    if not df.empty:
        collector.save_data(df, save_path=SAVE_PATH)

def collect_air_quality_data():
    """대기질 데이터 수집"""
    print("\n" + "=" * 70)
    print("4. 대기질 데이터 수집")
    print("=" * 70)

    collector = AirQualityCollector(api_key=API_KEYS['AIR_KOREA'])
    df = collector.collect_all_districts()

    if not df.empty:
        collector.save_data(df, save_path=SAVE_PATH)

def collect_school_data():
    """학교 데이터 수집"""
    print("\n" + "=" * 70)
    print("5. 학교 데이터 수집")
    print("=" * 70)

    collector = SchoolDataCollector(api_key=API_KEYS['SCHOOL'])
    df = collector.collect_all_schools()

    if not df.empty:
        collector.save_data(df, save_path=SAVE_PATH)

# ========================================
# 메인 실행
# ========================================

def main():
    """전체 데이터 수집 실행"""

    print("\n" + "=" * 70)
    print("서울시 아파트 가격 분석 - 데이터 수집 시작")
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 저장 폴더 생성
    os.makedirs(SAVE_PATH, exist_ok=True)

    # 데이터 수집 실행
    try:
        # 1. 아파트 실거래가 (시간이 가장 오래 걸림)
        collect_apartment_data()

        # 2. 지하철역
        collect_subway_data()

        # 3. 버스정류장
        collect_bus_data()

        # 4. 대기질
        collect_air_quality_data()

        # 5. 학교
        collect_school_data()

        print("\n" + "=" * 70)
        print("✅ 모든 데이터 수집이 완료되었습니다!")
        print(f"종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"저장 위치: {SAVE_PATH}")
        print("=" * 70)

        print("\n📋 수집된 파일 목록:")
        print("  1. seoul_apt_transactions_full.csv (아파트 실거래가)")
        print("  2. subway_stations.csv (지하철역)")
        print("  3. bus_stops.csv (버스정류장)")
        print("  4. air_quality.csv (대기질)")
        print("  5. schools.csv (학교)")

        print("\n📥 수동 다운로드 필요:")
        print("  1. crime_statistics.xlsx (범죄 통계)")
        print("  2. redevelopment_areas.csv (재개발/재건축)")
        print("  3. parks.csv (공원)")
        print("  4. college_admission_rate.xlsx (대학진학률)")

    except Exception as e:
        print(f"\n✗ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # API 키 확인
    missing_keys = [k for k, v in API_KEYS.items() if v.startswith('YOUR_')]

    if missing_keys:
        print("\n⚠️  API 키를 먼저 설정해주세요!")
        print(f"누락된 키: {', '.join(missing_keys)}")
        print("\n각 API 키 발급 방법:")
        print("  - MOLIT: https://www.data.go.kr/data/15057511/openapi.do")
        print("  - SEOUL: http://data.seoul.go.kr/")
        print("  - AIR_KOREA: https://www.data.go.kr/data/15073861/openapi.do")
        print("  - SCHOOL: https://www.data.go.kr/data/15021148/openapi.do")
    else:
        # 실행
        main()
