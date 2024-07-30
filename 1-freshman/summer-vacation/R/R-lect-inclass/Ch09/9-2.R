# library(ggmap)
# register_google(key='AIzaSyCK...E9urxjSpPOA')    # 구글키 등록

gc <- geocode(enc2utf8("설악산"))                  # 지점의 경도 위도
cen <- as.numeric(gc)                              # 경도 위도를 숫자로
map <- get_googlemap(center=cen,                   # 지도의 중심점 좌표
                     zoom=9,                       # 지도 확대 정도
                     size=c(640,640),              # 지도의 크기
                     maptype="roadmap")            # 지도의 유형
ggmap(map)                                         # 지도 화면에 보이기

map <- get_googlemap(center=cen,                   # 지도의 중심점 좌표
                     zoom=5,                       # 지도 확대 정도
                     size=c(640,640),              # 지도의 크기
                     maptype="roadmap")            # 지도의 유형
ggmap(map)                                         # 지도 화면에 보이기
