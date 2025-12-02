import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv
import pandas as pd

BASE_URL = 'https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
}

session = requests.Session()
session.headers.update(HEADERS)

url = BASE_URL
print(f"크롤링 중: {url}")

response = session.get(url, timeout=20)
responseText = response.text

# print('-'*50)
# print(response.status_code)
# print(response.text)

'''

# 파일 쓰기 (기존 파일이 있으면 덮어씀)
with open("./kobis.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("파일 저장 완료!")

'''

soup = BeautifulSoup(responseText, "html.parser")


# tag_table1 = soup.find('div', class_='rst_sch').find('table', class_='tbl_comm').find('tbody').find_all('tr')
tag_tr = soup.select('div.rst_sch table.tbl_comm tbody tr')

for tr in tag_tr:
    print('-'*50)
    #print(tr.text)

    영화정보 = {
        '영화명' : tr.select("tr td:nth-of-type(1) a")[0].get_text(strip=True),
        '영화명_영문' : tr.select("tr td:nth-of-type(2) a")[0].get_text(strip=True),
        '영화코드' : tr.select("tr td:nth-of-type(3)")[0].get_text(strip=True),
        '제작연도' : tr.select("tr td:nth-of-type(4)")[0].get_text(strip=True),
        '제작국가' : tr.select("tr td:nth-of-type(5)")[0].get_text(strip=True),
        '유형' : tr.select("tr td:nth-of-type(6)")[0].get_text(strip=True),
        '장르' : tr.select("tr td:nth-of-type(7)")[0].find('span')['title'].strip(),
        '제작상태' : tr.select("tr td:nth-of-type(8)")[0].get_text(strip=True),
        '감독' : tr.select("tr td:nth-of-type(9)")[0].get_text(strip=True),
        '제작사' : tr.select("tr td:nth-of-type(10)")[0].get_text(strip=True),
    }
    print(영화정보)











