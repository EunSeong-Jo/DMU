# library(ggmap)
# register_google(key='AIzaSyCK...E9urxjSpPOA')   # 구글키 등록

cen <- c(-118.233248, 34.085015)
map <- get_googlemap(center=cen)                  # 지도 생성
ggmap(map)                                        # 지도 화면에 보이기


# 구글 맵에서 장소를 클릭, 다시 틀릭

cen <- c(126.868108, 37.500672)
map <- get_googlemap(center=cen, zoom=18)                  # 지도 생성
ggmap(map)                                        # 지도 화면에 보이기
