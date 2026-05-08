import os
from dotenv import load_dotenv, find_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv(find_dotenv())

# API 키 가져오기
API_KEY = os.getenv("API_KEY")
print(API_KEY)  # 잘 불러와지는지 확인