"""
학교 정보 수집
출처: 교육부 학교알리미 API
"""

import requests
import pandas as pd
import xml.etree.ElementTree as ET
import os

class SchoolDataCollector:
    def __init__(self, api_key):
        """
        Parameters:
        -----------
        api_key : str
            학교알리미 API 키
            발급 URL: https://www.data.go.kr/data/15021148/openapi.do
        """
        self.api_key = api_key
        self.base_url = "https://open.neis.go.kr/hub"

    def fetch_schools(self, school_type='초등학교'):
        """
        서울시 학교 정보 수집

        Parameters:
        -----------
        school_type : str
            학교 종류 ('초등학교', '중학교', '고등학교')

        Returns:
        --------
        DataFrame
            학교 정보 (학교명, 위치)
        """
        # 학교급 코드 매핑
        school_codes = {
            '초등학교': '2',
            '중학교': '3',
            '고등학교': '4'
        }

        school_code = school_codes.get(school_type, '2')

        # API 엔드포인트
        endpoint = "/schoolInfo"
        url = f"{self.base_url}{endpoint}"

        params = {
            'KEY': self.api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 1000,
            'ATPT_OFCDC_SC_CODE': '11',  # 서울시 교육청 코드
            'SCHUL_KND_SC_NM': school_type
        }

        all_schools = []

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            # 데이터 추출
            if 'schoolInfo' in data:
                schools = data['schoolInfo'][1]['row']

                for school in schools:
                    school_data = {
                        '학교명': school.get('SCHUL_NM', ''),
                        '학교종류': school_type,
                        '설립구분': school.get('FOND_SC_NM', ''),
                        '소재지': school.get('ORG_RDNMA', ''),
                        '전화번호': school.get('ORG_TELNO', '')
                    }
                    all_schools.append(school_data)

                print(f"✓ {school_type}: {len(all_schools)}개 수집")

        except Exception as e:
            print(f"✗ {school_type} 수집 오류: {str(e)}")

        return pd.DataFrame(all_schools)

    def collect_all_schools(self):
        """
        초/중/고 전체 학교 정보 수집

        Returns:
        --------
        DataFrame
            전체 학교 정보
        """
        print("=" * 60)
        print("서울시 학교 정보 수집")
        print("=" * 60)

        all_data = []

        for school_type in ['초등학교', '중학교', '고등학교']:
            df = self.fetch_schools(school_type)
            all_data.append(df)

        # 통합
        df_total = pd.concat(all_data, ignore_index=True)

        print(f"\n✓ 총 {len(df_total)}개 학교 수집 완료")
        print(f"  - 초등학교: {len(df_total[df_total['학교종류']=='초등학교'])}개")
        print(f"  - 중학교: {len(df_total[df_total['학교종류']=='중학교'])}개")
        print(f"  - 고등학교: {len(df_total[df_total['학교종류']=='고등학교'])}개")

        return df_total

    def save_data(self, df, save_path='../data/raw'):
        """데이터 저장"""
        os.makedirs(save_path, exist_ok=True)
        filename = f"{save_path}/schools.csv"

        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n✓ 저장 완료: {filename}")

        return filename


# 사용 예시
if __name__ == "__main__":
    # API 키 설정
    API_KEY = "YOUR_SCHOOL_API_KEY"  # ← 학교알리미 API 키

    # 수집기 초기화
    collector = SchoolDataCollector(api_key=API_KEY)

    # 데이터 수집
    df = collector.collect_all_schools()

    # 데이터 저장
    if not df.empty:
        collector.save_data(df)
        print("\n✅ 학교 데이터 수집 완료!")
        print("\n[데이터 미리보기]")
        print(df.head(10))
    else:
        print("\n✗ 데이터 수집 실패")
