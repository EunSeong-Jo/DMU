"""
지하철역 정보 수집
출처: 서울시 열린데이터광장 API
"""

import requests
import pandas as pd
import json
import os

class SubwayDataCollector:
    def __init__(self, api_key):
        """
        Parameters:
        -----------
        api_key : str
            서울 열린데이터광장 API 키
            발급 URL: http://data.seoul.go.kr/
            API: "서울시 지하철역 정보"
        """
        self.api_key = api_key
        self.base_url = "http://openapi.seoul.go.kr:8088"

    def fetch_subway_stations(self):
        """
        서울시 지하철역 정보 수집

        Returns:
        --------
        DataFrame
            지하철역 정보 (역명, 호선, 위경도)
        """
        # API 엔드포인트
        service_name = "SearchSTNBySubwayLineInfo"
        start_idx = 1
        end_idx = 1000

        url = f"{self.base_url}/{self.api_key}/json/{service_name}/{start_idx}/{end_idx}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            # 데이터 추출
            if service_name in data:
                stations = data[service_name]['row']

                df = pd.DataFrame(stations)

                # 필요한 컬럼만 선택 및 이름 변경
                df_clean = df[[
                    'STATION_NM',   # 역명
                    'LINE_NUM',     # 호선
                    'XPOINT_WGS',   # 경도
                    'YPOINT_WGS'    # 위도
                ]].copy()

                df_clean.columns = ['역명', '호선', '경도', '위도']

                # 좌표를 숫자로 변환
                df_clean['경도'] = pd.to_numeric(df_clean['경도'], errors='coerce')
                df_clean['위도'] = pd.to_numeric(df_clean['위도'], errors='coerce')

                # 결측치 제거
                df_clean = df_clean.dropna()

                print(f"✓ 지하철역 {len(df_clean)}개 수집 완료")

                return df_clean
            else:
                print("✗ API 응답 오류")
                return pd.DataFrame()

        except Exception as e:
            print(f"✗ 오류 발생: {str(e)}")
            return pd.DataFrame()

    def save_data(self, df, save_path='../data/raw'):
        """
        데이터 저장

        Parameters:
        -----------
        df : DataFrame
            저장할 데이터
        save_path : str
            저장 경로
        """
        os.makedirs(save_path, exist_ok=True)
        filename = f"{save_path}/subway_stations.csv"

        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✓ 저장 완료: {filename}")
        print(f"  - 총 {len(df)}개 역")
        print(f"  - 호선: {df['호선'].unique()}")

        return filename


# 사용 예시
if __name__ == "__main__":
    # API 키 설정
    API_KEY = "YOUR_SEOUL_API_KEY"  # ← 서울시 열린데이터광장 API 키

    # 수집기 초기화
    collector = SubwayDataCollector(api_key=API_KEY)

    # 데이터 수집
    df = collector.fetch_subway_stations()

    # 데이터 저장
    if not df.empty:
        collector.save_data(df)
        print("\n✅ 지하철역 데이터 수집 완료!")
    else:
        print("\n✗ 데이터 수집 실패")

    # 데이터 미리보기
    if not df.empty:
        print("\n[데이터 미리보기]")
        print(df.head(10))
        print(f"\n호선별 역 개수:")
        print(df['호선'].value_counts())
