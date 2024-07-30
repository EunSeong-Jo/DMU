# library(ggmap)
# register_google(key='AIzaSyCK...E9urxjSpPOA') # 구글키 등록
library(ggplot2)

names <- c("용두암","성산일출봉","정방폭포",
           "중문관광단지","한라산1100고지","차귀도")
addr <- c("제주시 용두암길 15",
          "서귀포시 성산읍 성산리",
          "서귀포시 동홍동 299-3",
          "서귀포시 중문동 2624-1",
          "서귀포시 색달동 산1-2",
          "제주시 한경면 고산리 125")
gc <- geocode(enc2utf8(addr)) # 주소를 경도와 위도로 변환

gc
# 관광지 명칭과 좌표값으로 데이터프레임 생성
df <- data.frame(name=names,
                 lon=gc$lon,
                 lat=gc$lat)
df

cen <- c(mean(df$lon),mean(df$lat)) # 지도의 중심점
map <- get_googlemap(center=cen, # 지도 가져오기
                     maptype="roadmap", # 지도의 형태
                     zoom=10, # 지도의 확대 크기
                     size=c(640,640), # 지도의 크기
                     marker=gc) # 마커의 위치
ggmap(map) # 지도와 마커 화면에 보이기

# 명소 이름 지도 위에 표시하기
gmap <- ggmap(map)
gmap+geom_text(data=df, # 지도 위에 텍스트 표시
               aes(x=lon,y=lat), # 텍스트 위치(관광지 좌표)
               size=5, # 텍스트 크기
               label=df$name) # 텍스트 내용
