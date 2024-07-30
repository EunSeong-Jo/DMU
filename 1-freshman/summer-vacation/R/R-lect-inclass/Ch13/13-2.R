str(ds.total)
unique(ds.total$수집연월)         # 수집연월
unique(ds.total$상권업종대분류명) # 상권업종 대분류
unique(ds.total$상권업종중분류명) # 상권업종 중분류
unique(ds.total$상권업종소분류명) # 상권업종 소분류

# NA 포함여부 확인
sum(is.na(ds.total))

# 201712 수집 데이터만 추출
ds.201712 <- subset(ds.total, ds.total$수집연월== 5)
dim(ds.201712)

# 업종별 점포수(대분류)
store.level_1 <- aggregate(ds.201712[,1],
                           by=list(대분류=ds.201712$상권업종대분류명),
                           FUN=length)
store.level_1
names(store.level_1)[2] = c("count")
ggplot(store.level_1, aes(x=대분류, y=count)) +
  geom_bar(stat="identity", width=0.7, fill="steelblue") +
  ggtitle("업종별 점포수") +
  theme(plot.title = element_text(color="black", size=14, face="bold"))

# 구별 점포수
store.region <- aggregate(ds.201712[,1],
                          by=list(구이름=ds.201712$시군구명),
                          FUN=length)
store.region
names(store.region)[2] = c("count")

ggplot(store.region, aes(x=구이름, y=count)) +
  geom_bar(stat="identity", width=0.7, fill="steelblue") +
  ggtitle("구별 점포수") +
  theme(plot.title = element_text(color="black", size=14, face="bold"),
        axis.text.x = element_text(angle = 45, size=8))

# 지도 위에 구별 점포수 표시
store.region.loc <- aggregate(ds.201712[,c("경도","위도")],
                              by=list(구이름=ds.201712$시군구명),
                              FUN=mean)
store.region <- data.frame(store.region, store.region.loc[,2:3])

###################################################################
register_google(key='AIzaSyAswQPQN0KBAdgMDcxnKvwwiqJataTBpgM')
###################################################################

cen <- c(mean(store.region$경도),mean(store.region$위도))
map <- get_googlemap(center=cen,                 # 마커 없는 지도 가져오기
                     maptype="roadmap",
                     size=c(640,640),
                     zoom=11)
gmap <- ggmap(map)                               # 지도를 저장
gmap+geom_point(data=store.region,
                aes(x=경도,y=위도,size=count),
                alpha=0.5, col="red") +
  scale_size_continuous(range = c(1, 15))+       # 원의 크기 조절
  geom_text(data=store.region,                   # 지도 위에 텍스트 표시
            aes(x=경도,y=위도),                  # 텍스트 위치 (= 구의 좌표)
            size=3,                              # 텍스트 크기
            label=store.region$구이름)           # 텍스트 내용

# 점포수가 많은 상위 10개 동 확인
store.dong <- aggregate(ds.201712[,1],
                        by=list(동이름=ds.201712$행정동명),
                        FUN=length)
store.dong
names(store.dong)[2] = c("count")
store.dong <- store.dong[order(store.dong$count,decreasing=T),]
dong.top10 <- store.dong[1:10,]
dong.top10
ggplot(dong.top10, aes(x=reorder(동이름, -count), y=count)) +
  geom_bar(stat="identity", width=0.7, fill="steelblue") +
  ggtitle("점포수 많은 상위 10개동") +
  theme(plot.title = element_text(color="black", size=14, face="bold"),
        axis.text.x = element_text(angle = 45))
