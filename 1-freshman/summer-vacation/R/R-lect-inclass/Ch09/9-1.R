install.packages("ggmap")
library(ggmap)
library(ggplot2)

# 구글키 등록 
register_google(key='AIzaSyAswQPQN0...wwiqJataTBpgM')  

gc <- geocode(enc2utf8("종로구"))             # 지점의 경도 위도
gc
cen <- as.numeric(gc)                         # 경도 위도를 숫자로
cen

# 직접 입력
# cen <- c(126.97936, 37.57295)

map <- get_googlemap(center=cen)              # 지도 생성
ggmap(map)                                    # 지도 화면에 보이기
