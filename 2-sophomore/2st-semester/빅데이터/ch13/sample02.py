import pandas as pd
import requests
# pip install lxml
# pip install html5lib
# pip install beautifulsoup4

url = 'https://www.dongyang.ac.kr/dmu/4904/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZG11JTJGNjc3JTJGYXJ0Y2xMaXN0LmRvJTNG'
# -> 프로토콜: https
# -> 사이트대표주소: www.dongyang.ac.kr
# -> url(uri) : https://www.dongyang.ac.kr/dmu/4904/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZG11JTJGNjc3JTJGYXJ0Y2xMaXN0LmRvJTNG
# -> 사이트주소만: https://www.dongyang.ac.kr/dmu/4904/subview.do
# -> 파라미터: enc=Zm5jdDF8QEB8JTJGYmJzJTJGZG11JTJGNjc3JTJGYXJ0Y2xMaXN0LmRvJTNG
# -> 주소요청방식: get, post, delete, put, patch
# 주소로만 요청: get

# url = 'https://finance.naver.com/item/sise_day.naver?code=005930&page=1'
request_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=request_header)
print(response.status_code)
print(response.text)

raw_data = response.text
dy_data = pd.read_html(raw_data)

print(type(dy_data))

