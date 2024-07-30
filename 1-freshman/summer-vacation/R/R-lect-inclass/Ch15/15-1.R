setwd('D:/source')

ds <- read.csv('housing_price_King_County_extended.csv')

str(ds)
sum(is.na(ds))                        # 결측값 존재 확인

# 집값 분포
hist(ds$price/10000, main='집값 분포',
     xlab='집값(단위:만불)', ylab='주택수')
summary(ds$price/10000)
boxplot(ds$price/10000)

# 가장 비싼 주택과 가장 싼 주택
expensive <- ds[ds$price==max(ds$price),]
cheap <- ds[ds$price==min(ds$price),]
expensive
cheap

# 200만 불 이하 집값 분포
price200 <- ds$price/10000
price200 <- price200[price200<=200]
boxplot(price200)
hist(price200, main='주택 가격 분포',
     xlab='주택 가격(단위:만불)', ylab='주택수')

# 가격별 주택 분포 
library(ggmap)
library(RColorBrewer)

register_google(key='AIzaSyBLftN.....j9FKaJxf7T3wJY') 	# 구글키 등록
cen <- c(-122.073162, 47.521943)                        # 지도의 중심점
map <- get_googlemap(center=cen, 	                # 지도 가져오기
                     maptype="roadmap",
                     zoom=10)
gmap <- ggmap(map) 	                                # 가져온 지도 저장

# 데이터 샘플링
set.seed(1234)
idx <- sample(nrow(ds), 2000)
ds2000<- ds[idx,]

gmap1 <- gmap+geom_point(data=ds2000, 		
                         aes(x=long,y=lat, col=log(ds2000$price)),
                         size=3, alpha=0.5) +
  scale_color_gradient(low="yellow", high="red")
gmap1

# 지역별 주택 가격 
ds.agg <- aggregate(ds[,c('price','long','lat')], by=list(area=ds$zipcode), 
                    FUN=mean)
ds.agg

gmap2 <- gmap+geom_point(data=ds.agg, 		
                         aes(x=long,y=lat, col=log(ds.agg$price)),
                         size=8) +
  scale_color_gradient(low="yellow", high="red")
gmap2


# 200만 불 이상 주택의 분포
ds.high <- ds[ds$price>=2000000,]

gmap3 <- gmap+geom_point(data=ds.high, 		
                         aes(x=long,y=lat),
                         col='red', size=3) 
gmap3


# 20만불 이하 주택의 분포
ds.low <- ds[ds$price<=200000,]

gmap4 <- gmap+geom_point(data=ds.low, 		
                         aes(x=long,y=lat),
                         col='blue', size=3) 
gmap4
