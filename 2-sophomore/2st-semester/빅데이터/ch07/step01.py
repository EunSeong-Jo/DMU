# kobis_movie_scraper.py
# KOBIS 영화목록(검색결과) 페이지를 순회하며 영화정보 스크래핑 -> CSV 저장
# Python 3.8+
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

def parse_movie_rows(soup):
    """
    페이지 내 영화 목록 테이블에서 각 행을 파싱하여 dict 리스트로 반환
    (페이지 레이아웃 변경 시 선택자 조정 필요)
    """
    movies = []
    # 페이지 구조에 따라 table/ tbody 가 다를 수 있음 — robust하게 tr 찾기
    # 보통 검색 결과는 <table> 내부에 <tbody>와 여러 <tr>로 구성됨
    # 아래는 일반적인 테이블 행 파싱 방법입니다.
    table = soup.find("table")
    if not table:
        return movies

    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")
    for r in rows:
        cols = [td.get_text(strip=True) for td in r.find_all(["td","th"])]
        # 컬럼 수나 순서는 사이트 변경에 따라 달라질 수 있으므로
        # 가능한 컬럼들을 안전하게 매핑 (예시)
        if not cols or len(cols) < 3:
            continue
        # 대략적인 칼럼: 영화명, 영화명(영문), 영화코드, 제작연도, 제작국가, 유형, 장르, 제작상태, 감독, 제작사 ...
        movie = {
            "raw_columns": cols,
        }
        # try to populate some common fields if available
        # many KOBIS 결과는 "영화명 | 영화명(영문) | 영화코드 | 제작연도 | 제작국가 | 유형 | 장르 | 제작상태 | 감독 | 제작사"
        if len(cols) >= 10:
            movie.update({
                "movieName": cols[0],
                "movieNameEn": cols[1],
                "movieCode": cols[2],
                "productionYear": cols[3],
                "productionCountry": cols[4],
                "movieType": cols[5],
                "genre": cols[6],
                "productionStatus": cols[7],
                "director": cols[8],
                "company": cols[9],
            })
        movies.append(movie)
    return movies

def find_next_page_url(soup, current_url):
    """
    페이지 하단의 '다음' 또는 페이지네이션 링크에서 다음 페이지 href를 찾아 반환.
    href가 상대경로일 수 있으므로 urljoin으로 절대화 함.
    반환값: 다음 페이지 URL 문자열 또는 None
    """
    # 1) '다음' 텍스트를 가진 a 태그 찾기
    a_next = soup.find("a", string=lambda s: s and "다음" in s)
    if a_next and a_next.get("href"):
        return urljoin(current_url, a_next["href"])

    # 2) 숫자 페이지 링크 중 현재 페이지 다음 링크를 찾아서 반환 (fallback)
    # 찾기: .paging 또는 .pg 등 페이지네이션을 묶는 요소 추정
    pagination = soup.find(class_=lambda x: x and "page" in x.lower() or x and "paging" in x.lower())
    if pagination:
        # 현재 active 페이지 찾기
        active = pagination.find(class_=lambda x: x and ("on" in x or "active" in x))
        if active:
            # 다음 sibling의 링크 사용
            nxt = active.find_next("a")
            if nxt and nxt.get("href"):
                return urljoin(current_url, nxt["href"])
    # 3) a 태그들 중 ">" 같은 심볼 링크 찾아보기
    a_gt = soup.find("a", string=lambda s: s and (">" in s or "»" in s))
    if a_gt and a_gt.get("href"):
        return urljoin(current_url, a_gt["href"])

    return None

def scrape_all(start_url=BASE_URL, delay=0.8, max_pages=None):
    """
    start_url에서 시작하여 다음 페이지를 따라가며 영화정보를 모두 수집.
    delay: 각 요청 사이 대기시간(초)
    max_pages: None이면 마지막까지, 정수면 최대 그 페이지 수만큼
    반환: pandas.DataFrame
    """
    session = requests.Session()
    session.headers.update(HEADERS)

    url = start_url
    all_movies = []
    page_count = 0

    while url:
        print(f"크롤링 중: {url}")
        resp = session.get(url, timeout=20)
        if resp.status_code != 200:
            print(f"경고: HTTP {resp.status_code} — 중단")
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        movies = parse_movie_rows(soup)
        print(f"  발견된 영화행: {len(movies)}")
        all_movies.extend(movies)

        page_count += 1
        if max_pages and page_count >= max_pages:
            print("최대 페이지 수에 도달하여 종료")
            break

        next_url = find_next_page_url(soup, url)
        if not next_url:
            print("다음 페이지 없음 — 완료")
            break

        # 안전한 요청 빈도 유지
        time.sleep(delay)
        url = next_url

    # DataFrame으로 정리 (raw_columns는 유지)
    df = pd.DataFrame(all_movies)
    return df

def main():
    df = scrape_all(max_pages=50)  # 필요시 max_pages를 설정 (None이면 끝까지)
    print(f"총 수집 레코드: {len(df)}")
    # CSV 저장
    out_csv = "kobis_movies.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"CSV로 저장됨: {out_csv}")

if __name__ == "__main__":
    main()
