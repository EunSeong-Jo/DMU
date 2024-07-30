head(ds)

ds.yeoksam <- subset(ds.total, 
                     ds.total$수집연월==5 & ds.total$행정동명=="역삼1동")

head(ds.yeoksam)

# 점포를 업종별로 구분하여 지도에 표시
cen <- c(mean(ds.yeoksam$경도), mean(ds.yeoksam$위도))
map <- get_googlemap(center=cen,         # 마커 없는 지도 가져오기
                     maptype="roadmap",
                     size=c(640,640),
                     zoom=15)
gmap <- ggmap(map)                       # 지도를 저장

gmap + 
  geom_point(data = ds.yeoksam,
             aes(x=경도, y=위도, color=상권업종대분류명),
             size=2, alpha=0.7) +
  labs(x = "Longitude", y = "Latitude",
       title="역삼1동 업종별 점포", color = "업종")

# 커피 점포만 지도에 표시
ds.yeoksam2 <- subset(ds.yeoksam, 
                      ds.yeoksam$상권업종소분류명=="커피전문점/카페/다방")
gmap + 
  geom_point(data = ds.yeoksam2,
             aes(x=경도, y=위도), size=2, alpha=0.5, col="red") +
  labs(x = "Longitude", y = "Latitude", title="역삼1동 커피점" )
