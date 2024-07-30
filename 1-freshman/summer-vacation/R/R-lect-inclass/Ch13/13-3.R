# 업종별 점포수의 변화
store.change <- aggregate(ds.total[,1],
                          by=list(연월=ds.total$수집연월,
                                  업종대분류=ds.total$상권업종대분류명),
                          FUN=length)
head(store.change)
names(store.change)[3] <- c("count")
str(store.change)
files

ggplot(store.change, aes(x=연월, y=count, colour=업종대분류, group=업종대분류)) +
  geom_line() +
  geom_point(size=6, shape=19, alpha=0.5) +
  ggtitle("업종별 점포수 변화 (대분류)") +
  ylab("점포수") +
  scale_x_continuous(breaks=1:5, labels=files) +
  theme(plot.title = element_text(color="black", size=14, face="bold"))

# 점포수 변화가 큰 상위 10개 업종
store.tmp <- aggregate(ds.total[,1],
                       by=list(연월=ds.total$수집연월,
                               업종소분류=ds.total$상권업종소분류명),
                       FUN=length)
names(store.tmp)[3] <- c("count")
store.201512 <- store.tmp[store.tmp$연월==1,]
names(store.201512)[3] <- c("cnt_2015")
store.201712 <- store.tmp[store.tmp$연월==5,]
names(store.201712)[3] <- c("cnt_2017")

store.diff <- merge(store.201512[,2:3], store.201712[,2:3])
store.diff$diff <- abs(store.diff$cnt_2015-store.diff$cnt_2017)
store.diff <- store.diff[order(by=store.diff$diff, decreasing=T),]
str(store.diff)

top10 <- store.diff[1:10,1] # 업종명
top10

store.change <- subset(store.tmp, store.tmp$업종소분류 %in% top10)
ggplot(store.change, aes(x=연월, y=count, colour=업종소분류, group=업종소분류)) +
  geom_line() +
  geom_point(size=6, shape=19, alpha=0.5) +
  ggtitle("점포수 변화 Top 10 업종(소분류)") +
  ylab("점포수") +
  scale_x_continuous(breaks=1:5,
                     labels=files) +
  theme(plot.title = element_text(color="black", size=14, face="bold"))

# 구별 점포수의 변화
store.gu <- aggregate(ds.total[,1],
                      by=list(연월=ds.total$수집연월,
                              구이름=ds.total$시군구명),
                      FUN=length)
names(store.gu)[3] <- c("count")
str(store.gu)
head(store.gu)

ggplot(store.gu, aes(x=연월, y=count, colour=구이름, group=구이름)) +
  geom_line() +
  geom_point(size=6, shape=19, alpha=0.5) +
  ggtitle("구별 점포수 변화 (대분류)") +
  ylab("점포수") +
  scale_x_continuous(breaks=1:5, labels=files) +
  theme(plot.title = element_text(color="black", size=14, face="bold"))

# 점포수 변화가 큰 상위 10개 동
store.tmp <- aggregate(ds.total[,1],
                       by=list(연월=ds.total$수집연월,
                               동이름=ds.total$행정동명),
                       FUN=length)
names(store.tmp)[3] <- c("count")
store.dong.201512 <- store.tmp[store.tmp$연월==1,]
names(store.dong.201512)[3] <- c("cnt_2015")
store.dong.201712 <- store.tmp[store.tmp$연월==5,]
names(store.dong.201712)[3] <- c("cnt_2017")
store.diff <- merge(store.dong.201512[,2:3], store.dong.201712[,2:3])
store.diff$diff <- abs(store.diff$cnt_2015-store.diff$cnt_2017)
store.diff <- store.diff[order(by=store.diff$diff, decreasing=T),]

top10 <- store.diff[1:10,1]                # 동명
top10
store.change <- subset(store.tmp, store.tmp$동이름 %in% top10)
ggplot(store.change, aes(x=연월, y=count, colour=동이름, group=동이름)) +
  geom_line() +
  geom_point(size=6, shape=19, alpha=0.5) +
  ggtitle("점포수 변화 Top 10 동") +
  ylab("점포수") +
  scale_x_continuous(breaks=1:5, labels=files) +
  theme(plot.title = element_text(color="black", size=14, face="bold"))
