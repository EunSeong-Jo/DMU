"""
KOBIS API searchMovieList 테스트
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('KOBIS_API_KEY')
base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest"

# 영화 목록 조회 API 테스트
url = f"{base_url}/movie/searchMovieList.json"

# 테스트 1: repNationCd 없이
params = {
    'key': api_key,
    'openStartDt': '2019',
    'openEndDt': '2019',
    'curPage': 1,
    'itemPerPage': 10
}

print(f"[TEST] KOBIS searchMovieList API 테스트")
print(f"URL: {url}")
print(f"Params: {json.dumps(params, indent=2, ensure_ascii=False)}")
print()

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    print(f"[OK] API 응답 성공")
    print(f"응답 데이터:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"[ERROR] API 요청 실패: {e}")
    print(f"Response text: {response.text if 'response' in locals() else 'N/A'}")
