"""
버스정류장 정보 수집
출처: 서울시 열린데이터광장 API
"""

import requests
import pandas as pd
import os

class BusStopCollector:
    def __init__(self, api_key):
        """
        Parameters:
        -----------
        api_key : str
            서울 열린데이터광장 API 키
        """
        self.api_key = api_key
        self.base_url = "http://openapi.seoul.go.kr:8088"

    def fetch_bus_stops(self):
        """
        서울시 버스정류장 정보 수집

        Returns:
        --------
        DataFrame
            버스정류장 정보 (정류장명, 위경도)
        """
        service_name = "StationLocationInfo"

        all_stops = []
        start_idx = 1
        batch_size = 1000

        print("버스정류장 데이터 수집 중...")

        while True:
            end_idx = start_idx + batch_size - 1
            url = f"{self.base_url}/{self.api_key}/json/{service_name}/{start_idx}/{end_idx}"

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                if service_name not in data:
                    break

                result = data[service_name]

                # 더 이상 데이터가 없으면 종료
                if 'row' not in result:
                    break

                stops = result['row']
                all_stops.extend(stops)

                print(f"  수집: {start_idx}~{end_idx} ({len(stops)}개)")

                # 마지막 배치인지 확인
                if len(stops) < batch_size:
                    break

                start_idx = end_idx + 1

            except Exception as e:
                print(f"✗ 오류 발생: {str(e)}")
                break

        if all_stops:
            df = pd.DataFrame(all_stops)

            # 필요한 컬럼만 선택
            df_clean = df[[
                'STOP_NM',      # 정류장명
                'GPS_X',        # 경도
                'GPS_Y'         # 위도
            ]].copy()

            df_clean.columns = ['정류장명', '경도', '위도']

            # 좌표 변환
            df_clean['경도'] = pd.to_numeric(df_clean['경도'], errors='coerce')
            df_clean['위도'] = pd.to_numeric(df_clean['위도'], errors='coerce')

            # 결측치 제거
            df_clean = df_clean.dropna()

            print(f"\n✓ 버스정류장 {len(df_clean):,}개 수집 완료")
            return df_clean
        else:
            print("✗ 데이터 없음")
            return pd.DataFrame()

    def save_data(self, df, save_path='../data/raw'):
        """데이터 저장"""
        os.makedirs(save_path, exist_ok=True)
        filename = f"{save_path}/bus_stops.csv"

        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✓ 저장 완료: {filename}")
        print(f"  - 총 {len(df):,}개 정류장")

        return filename


# 사용 예시
if __name__ == "__main__":
    # API 키 설정
    API_KEY = "YOUR_SEOUL_API_KEY"  # ← 서울시 API 키

    # 수집기 초기화
    collector = BusStopCollector(api_key=API_KEY)

    # 데이터 수집
    df = collector.fetch_bus_stops()

    # 데이터 저장
    if not df.empty:
        collector.save_data(df)
        print("\n✅ 버스정류장 데이터 수집 완료!")
        print(f"\n[데이터 미리보기]")
        print(df.head(10))
    else:
        print("\n✗ 데이터 수집 실패")
