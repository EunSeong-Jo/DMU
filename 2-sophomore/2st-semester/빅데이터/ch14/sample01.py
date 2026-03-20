from io import StringIO

import pandas as pd
import requests
from fontTools.ttLib.tables.E_B_L_C_ import table_E_B_L_C_

# pip install lxml
# pip install html5lib
# pip install beautifulsoup4

# http(https), ftp(sftp), smtp....
# 네트워크: 전송 -> ip, port, instance, account, password
# 211.123.12.12(ip v4) ->v6
# 동양미래대학교 -> 203.249.39.43 => www.dongyang.ac.kr(도메인) => 도메인서버(dns서버)
# http -> 80, https -> 443
# *.php, *.aspx, *.jsp, *.do, *.naver (스프링, 전자정부프레임워크) -> .do

url = 'https://www.dongyang.ac.kr/dmu/4904/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZG11JTJGNjc3JTJGYXJ0Y2xMaXN0LmRvJTNG'
# -> 프로토콜: https
# -> 사이트대표주소: www.dongyang.ac.kr
# -> url(uri) : https://www.dongyang.ac.kr/dmu/4904/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZG11JTJGNjc3JTJGYXJ0Y2xMaXN0LmRvJTNG
# -> 사이트주소만: https://www.dongyang.ac.kr/dmu/4904/subview.do
# -> 파라미터: enc=Zm5jdDF8QEB8JTJGYmJzJTJGZG11JTJGNjc3JTJGYXJ0Y2xMaXN0LmRvJTNG
# -> 주소요청방식: get, post, delete, put, patch
# 주소로만 요청: get

request_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=request_header)

print(response.status_code)
print(response.text)

raw_data = response.text

dy_data = pd.read_html(StringIO(raw_data))
print('-'*50)
print(type(dy_data))
print(len(dy_data))

table_data = dy_data[0]
print('-'*50)
print(type(table_data))

print(table_data.info())
print(table_data.head())

