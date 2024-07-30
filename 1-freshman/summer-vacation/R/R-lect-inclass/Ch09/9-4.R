# library(ggmap)
# register_google(key='AIzaSyCK...E9urxjSpPOA')   # 구글키 등록

gc <- geocode(enc2utf8("용인"))                   # 지점의 경도와 위도
cen <- as.numeric(gc)                             # 경도와 위도를 숫자로
map <- get_googlemap(center=cen,                  # 지도의 중심
                     maptyp="roadmap",            # 지도의 형태
                     marker=gc)                   # 마커의 위치
ggmap(map)                                        # 지도 화면에 보이기
