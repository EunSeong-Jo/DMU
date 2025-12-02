"""
대기질 정보 수집
출처: 한국환경공단 에어코리아 API
"""

import requests
import pandas as pd
import os
from datetime import datetime

class AirQualityCollector:
    def __init__(self, api_key):
        """
        Parameters:
        -----------
        api_key : str
            에어코리아 API 키
            발급 URL: https://www.data.go.kr/data/15073861/openapi.do
        """
        self.api_key = api_key
        self.base_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc"

        # 서울시 25개 구별 측정소 매핑
        self.district_stations = {
            '강남구': '강남구',
            '강동구': '강동구',
            '강북구': '강북구',
            '강서구': '강서구',
            '관악구': '관악구',
            '광진구': '광진구',
            '구로구': '구로구',
            '금천구': '금천구',
            '노원구': '노원구',
            '도봉구': '도봉구',
            '동대문구': '동대문구',
            '동작구': '동작구',
            '마포구': '마포구',
            '서대문구': '서대문구',
            '서초구': '서초구',
            '성동구': '성동구',
            '성북구': '성북구',
            '송파구': '송파구',
            '양천구': '양천구',
            '영등포구': '영등포구',
            '용산구': '용산구',
            '은평구': '은평구',
            '종로구': '종로구',
            '중구': '중구',
            '중랑구': '중랑구'
        }

    def fetch_air_quality(self, station_name, num_of_rows=100):
        """
        특정 측정소의 대기질 정보 수집

        Parameters:
        -----------
        station_name : str
            측정소명
        num_of_rows : int
            조회할 데이터 개수

        Returns:
        --------
        dict
            평균 대기질 정보
        """
        url = f"{self.base_url}/getMsrstnAcctoRltmMesureDnsty"

        params = {
            'serviceKey': self.api_key,
            'returnType': 'json',
            'numOfRows': num_of_rows,
            'pageNo': 1,
            'stationName': station_name,
            'dataTerm': 'MONTH',  # 최근 1개월
            'ver': '1.0'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if 'response' in data and 'body' in data['response']:
                items = data['response']['body']['items']

                if items:
                    # 평균 계산
                    pm10_values = []
                    pm25_values = []

                    for item in items:
                        try:
                            pm10 = float(item.get('pm10Value', 0))
                            pm25 = float(item.get('pm25Value', 0))

                            if pm10 > 0:
                                pm10_values.append(pm10)
                            if pm25 > 0:
                                pm25_values.append(pm25)
                        except:
                            continue

                    result = {
                        'PM10_평균': sum(pm10_values) / len(pm10_values) if pm10_values else None,
                        'PM25_평균': sum(pm25_values) / len(pm25_values) if pm25_values else None,
                        '데이터_개수': len(items)
                    }

                    print(f"✓ {station_name}: PM10={result['PM10_평균']:.1f}, PM2.5={result['PM25_평균']:.1f}")
                    return result

        except Exception as e:
            print(f"✗ {station_name}: 오류 - {str(e)}")
            return None

    def collect_all_districts(self):
        """
        서울시 전체 구의 대기질 정보 수집

        Returns:
        --------
        DataFrame
            구별 평균 대기질 정보
        """
        print("=" * 60)
        print("서울시 구별 대기질 정보 수집")
        print("=" * 60)

        results = []

        for district, station in self.district_stations.items():
            air_data = self.fetch_air_quality(station)

            if air_data:
                results.append({
                    '구': district,
                    '측정소': station,
                    'PM10_평균': air_data['PM10_평균'],
                    'PM2.5_평균': air_data['PM25_평균'],
                    '데이터_개수': air_data['데이터_개수']
                })

        df = pd.DataFrame(results)

        print(f"\n✓ 총 {len(df)}개 구 대기질 정보 수집 완료")

        return df

    def save_data(self, df, save_path='../data/raw'):
        """데이터 저장"""
        os.makedirs(save_path, exist_ok=True)
        filename = f"{save_path}/air_quality.csv"

        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n✓ 저장 완료: {filename}")

        return filename


# 사용 예시
if __name__ == "__main__":
    # API 키 설정
    API_KEY = "YOUR_AIR_KOREA_API_KEY"  # ← 에어코리아 API 키

    # 수집기 초기화
    collector = AirQualityCollector(api_key=API_KEY)

    # 데이터 수집
    df = collector.collect_all_districts()

    # 데이터 저장
    if not df.empty:
        collector.save_data(df)
        print("\n✅ 대기질 데이터 수집 완료!")
        print("\n[데이터 미리보기]")
        print(df.head(10))
        print(f"\n[통계]")
        print(df[['PM10_평균', 'PM2.5_평균']].describe())
    else:
        print("\n✗ 데이터 수집 실패")
