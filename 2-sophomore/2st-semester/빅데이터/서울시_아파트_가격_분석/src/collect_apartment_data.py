"""
아파트 실거래가 데이터 수집
출처: 국토교통부 실거래가 공개시스템 API
"""

import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import os

class ApartmentDataCollector:
    def __init__(self, api_key):
        """
        Parameters:
        -----------
        api_key : str
            공공데이터포털에서 발급받은 API 키
            발급 URL: https://www.data.go.kr/data/15057511/openapi.do
        """
        self.api_key = api_key
        self.base_url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"

        # 서울시 25개 구 법정동코드
        self.seoul_districts = {
            '강남구': '11680', '강동구': '11740', '강북구': '11305', '강서구': '11500',
            '관악구': '11620', '광진구': '11215', '구로구': '11530', '금천구': '11545',
            '노원구': '11350', '도봉구': '11320', '동대문구': '11230', '동작구': '11590',
            '마포구': '11440', '서대문구': '11410', '서초구': '11650', '성동구': '11200',
            '성북구': '11290', '송파구': '11710', '양천구': '11470', '영등포구': '11560',
            '용산구': '11170', '은평구': '11380', '종로구': '11110', '중구': '11140',
            '중랑구': '11260'
        }

    def fetch_data(self, year, month, district_code):
        """
        특정 연월, 지역의 아파트 실거래가 데이터 수집

        Parameters:
        -----------
        year : int
            연도 (예: 2024)
        month : int
            월 (1-12)
        district_code : str
            법정동코드 (예: '11680' for 강남구)

        Returns:
        --------
        list of dict
            거래 데이터 리스트
        """
        params = {
            'serviceKey': self.api_key,
            'LAWD_CD': district_code,
            'DEAL_YMD': f"{year}{month:02d}",
            'numOfRows': '1000'  # 한 번에 최대 1000건
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            # XML 파싱
            root = ET.fromstring(response.content)
            items = root.findall('.//item')

            data_list = []
            for item in items:
                data = {
                    '거래금액': item.findtext('dealAmount', '').strip(),
                    '건축연도': item.findtext('buildYear', ''),
                    '년': item.findtext('dealYear', ''),
                    '월': item.findtext('dealMonth', ''),
                    '일': item.findtext('dealDay', ''),
                    '전용면적': item.findtext('excluUseAr', ''),
                    '지번': item.findtext('jibun', ''),
                    '지역코드': item.findtext('cdealType', ''),
                    '법정동': item.findtext('umdNm', ''),
                    '아파트명': item.findtext('aptNm', ''),
                    '층': item.findtext('floor', ''),
                    '구': item.findtext('rgdNm', ''),  # 등록일
                    '도로명': item.findtext('roadNm', ''),
                }
                data_list.append(data)

            print(f"✓ {year}-{month:02d} {district_code}: {len(data_list)}건 수집")
            return data_list

        except Exception as e:
            print(f"✗ {year}-{month:02d} {district_code}: 오류 발생 - {str(e)}")
            return []

    def collect_all(self, start_year=2020, end_year=2024, save_path='../data/raw'):
        """
        전체 데이터 수집 (서울시 25개 구, 지정 기간)

        Parameters:
        -----------
        start_year : int
            시작 연도
        end_year : int
            종료 연도
        save_path : str
            저장 경로
        """
        all_data = []
        total_requests = 0

        print("=" * 60)
        print("아파트 실거래가 데이터 수집 시작")
        print(f"기간: {start_year}년 ~ {end_year}년")
        print(f"지역: 서울시 25개 구")
        print("=" * 60)

        for year in range(start_year, end_year + 1):
            # 현재 연도라면 현재 월까지만
            max_month = datetime.now().month if year == datetime.now().year else 12

            for month in range(1, max_month + 1):
                for district_name, district_code in self.seoul_districts.items():
                    data = self.fetch_data(year, month, district_code)

                    # 구 이름 추가
                    for item in data:
                        item['구'] = district_name

                    all_data.extend(data)
                    total_requests += 1

                    # API 호출 제한 고려 (초당 최대 요청 수 제한)
                    time.sleep(0.1)  # 100ms 대기

                # 월별로 중간 저장
                if len(all_data) > 10000:
                    self._save_intermediate(all_data, year, month, save_path)
                    all_data = []

        # 최종 저장
        if all_data:
            df = pd.DataFrame(all_data)
            self._save_final(df, save_path)

        print("\n" + "=" * 60)
        print(f"데이터 수집 완료!")
        print(f"총 API 요청: {total_requests}회")
        print(f"총 데이터: {len(all_data):,}건")
        print("=" * 60)

    def _save_intermediate(self, data_list, year, month, save_path):
        """중간 저장"""
        df = pd.DataFrame(data_list)
        os.makedirs(save_path, exist_ok=True)
        filename = f"{save_path}/apt_trade_{year}_{month:02d}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"  → 중간 저장: {filename}")

    def _save_final(self, df, save_path):
        """최종 저장"""
        os.makedirs(save_path, exist_ok=True)

        # 데이터 전처리
        df['거래금액'] = df['거래금액'].str.replace(',', '').str.strip()
        df['거래금액(억)'] = pd.to_numeric(df['거래금액'], errors='coerce') / 10000
        df['전용면적'] = pd.to_numeric(df['전용면적'], errors='coerce')
        df['건축연도'] = pd.to_numeric(df['건축연도'], errors='coerce')
        df['층'] = pd.to_numeric(df['층'], errors='coerce')

        # 거래일자 생성
        df['거래일자'] = pd.to_datetime(
            df['년'].astype(str) + '-' +
            df['월'].astype(str).str.zfill(2) + '-' +
            df['일'].astype(str).str.zfill(2),
            errors='coerce'
        )

        # 건축연령 계산
        df['건축연령'] = datetime.now().year - df['건축연도']

        filename = f"{save_path}/seoul_apt_transactions_full.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n최종 저장: {filename}")
        print(f"데이터 shape: {df.shape}")

        return df


# 사용 예시
if __name__ == "__main__":
    # API 키 설정 (공공데이터포털에서 발급)
    API_KEY = "YOUR_API_KEY_HERE"  # ← 여기에 발급받은 키 입력

    # 수집기 초기화
    collector = ApartmentDataCollector(api_key=API_KEY)

    # 데이터 수집 실행
    collector.collect_all(
        start_year=2020,
        end_year=2024,
        save_path='../data/raw'
    )

    print("\n✅ 데이터 수집이 완료되었습니다!")
    print("📁 저장 위치: data/raw/seoul_apt_transactions_full.csv")
