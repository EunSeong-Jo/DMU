import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # 진행률 표시용 (선택사항)

url = "https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/141.0.0.0 Safari/537.36",
    "Referer": "https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do",
    "Origin": "https://www.kobis.or.kr",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

# ⚠️ CSRFToken은 페이지 로드 시마다 바뀌므로 실제 사용 시는 requests.get()으로 가져와야 함
CSRF_TOKEN = "ZCMVMJMfMd2aoS39ntgNv4E6kJ9IGJHiGiXS1ew2W-Q"

def fetch_page(page: int):
    """한 페이지를 요청하고 영화정보 리스트 반환"""
    data = {
        "CSRFToken": CSRF_TOKEN,
        "curPage": str(page),
        "useYn": "Y",
    }

    response = requests.post(url, headers=headers, data=data, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    tag_tr = soup.select("div.rst_sch table.tbl_comm tbody tr")

    page_movies = []
    for tr in tag_tr:
        try:
            tds = tr.select("td")
            영화정보 = {
                '영화명': tds[0].get_text(strip=True),
                '영화명_영문': tds[1].get_text(strip=True),
                '영화코드': tds[2].get_text(strip=True),
                '제작연도': tds[3].get_text(strip=True),
                '제작국가': tds[4].get_text(strip=True),
                '유형': tds[5].get_text(strip=True),
                '장르': tds[6].find('span')['title'] if tds[6].find('span') else '',
                '제작상태': tds[7].get_text(strip=True),
                '감독': tds[8].get_text(strip=True),
                '제작사': tds[9].get_text(strip=True),
            }
            page_movies.append(영화정보)
        except Exception as e:
            print(f"[ERROR] page {page} tr parse error: {e}")
    return page_movies


def main():
    max_page = 11459 + 1  # ⚠️ 테스트 시 너무 크지 않게. 실제는 11459 + 1
    all_movies = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        # 비동기 작업 등록
        futures = {executor.submit(fetch_page, page): page for page in range(1, max_page + 1)}

        for future in tqdm(as_completed(futures), total=len(futures), desc="크롤링 진행중"):
            try:
                result = future.result()
                all_movies.extend(result)
            except Exception as e:
                page = futures[future]
                print(f"[ERROR] 페이지 {page} 처리 실패: {e}")

    # CSV 저장
    df = pd.DataFrame(all_movies)
    df.to_csv("movie_list.csv", index=False, encoding="utf-8")
    print(f"✅ 완료! 총 {len(all_movies)}건 저장됨.")


if __name__ == "__main__":
    main()
