install.packages("ggmap")
library(ggmap)
library(ggplot2)

# 구글키 등록 
# register_google(key='AIzaSyCK...E9urxjSpPOA')  

str(wind)
head(wind)

# 데이터 준비
sp <- sample(1:nrow(wind),50)                    # 50개 데이터 샘플링
df <- wind[sp,]
head(df)

cen <- c(mean(df$lon), mean(df$lat))             # 지도의 중심점 계산
gc <- data.frame(lon=df$lon, lat=df$lat)         # 측정 위치 좌표값 데이터
head(gc)

# 측정 위치에 마커 표시하기
map <- get_googlemap(center=cen,
                     maptype="roadmap",
                     zoom=6,
                     marker=gc)
ggmap(map)

# 풍속을 원의 크기로 표시하기
map <- get_googlemap(center=cen,                 # 마커 없는 지도 가져오기
                     maptype="roadmap",
                     zoom=6)
gmap <- ggmap(map)                               # 지도를 저장
gmap+geom_point(data=df,                         # 풍속을 원의 크기로 표시
                aes(x=lon,y=lat,size=spd),
                alpha=0.5,
                col="blue") +
  scale_size_continuous(range = c(1, 14))        # 원의 크기 조절

gmap+geom_point(data=df,                         # 풍속을 원의 크기로 표시
                aes(x=lon,y=lat,size=spd),
                alpha=0.3,
                col="blue") +
  scale_size_continuous(range = c(1, 14))        # 원의 크기 조절
