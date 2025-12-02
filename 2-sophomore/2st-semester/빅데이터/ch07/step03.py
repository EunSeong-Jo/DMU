import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv
import pandas as pd

url = "https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/141.0.0.0 Safari/537.36",
    "Referer": "https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do",
    "Origin": "https://www.kobis.or.kr",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

# POST로 보낼 폼데이터 (Network 탭에 있던 것 그대로)
data = {
    "CSRFToken": "ZCMVMJMfMd2aoS39ntgNv4E6kJ9IGJHiGiXS1ew2W-Q",  # 이 값은 페이지 로드 시마다 바뀜
    "curPage": "2",          # 페이지 번호 (변경 가능)
    "useYn": "Y",
}

max_page = 11459 + 1
# max_page = 3
영화정보_리스트 = []

for page in range(1, max_page):
    print(f'{page}/{max_page}')
    data['curPage'] = str(page)

    # 요청 보내기
    response = requests.post(url, headers=headers, data=data)
    responseText = response.text

    # print('-'*50)
    # print(response.status_code)
    # print(response.text)

    soup = BeautifulSoup(responseText, "html.parser")

    tag_tr = soup.select('div.rst_sch table.tbl_comm tbody tr')

    for tr in tag_tr:
        # print('-'*50)
        # print(tr.text)

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
        영화정보_리스트.append(영화정보)

# print(영화정보_리스트)

# DataFrame으로 변환
df = pd.DataFrame(영화정보_리스트)

# CSV 파일로 저장
df.to_csv("./movie_list.csv", index=False, encoding="utf-8")









