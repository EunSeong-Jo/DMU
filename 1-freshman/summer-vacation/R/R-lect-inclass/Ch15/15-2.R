MYCOR <- function(ds.group) {
  corr <- cor(ds.group[,1], ds.group[,-1])
  odr <- order(corr[1,], decreasing = T)
  corr.sort <- corr[odr]
  names(corr.sort) <- colnames(corr)[odr]
  return(round(corr.sort,3))
} 

# 불필요한 열 제거
ds.pure <- ds[,-c(1,2, 17)]

# 상관 분석
MYCOR(ds.pure) 

# 건평과 집값의 산점도
plot(ds.pure$sqft_living, ds.pure$price/10000,
     main='건평과 집값', xlab='건평', ylab='집값(만불)')
model <- lm(price/10000~sqft_living, ds.pure)
abline(model, col='red')

# 주택을 가격에 따라 3개 그룹(High, Middle, Low)으로 나눔
summary(ds.pure$price)
ds.pure$group <- 'Middle'
ds.pure$group[ds.pure$price>=645000] <- 'High'
ds.pure$group[ds.pure$price<=321950] <- 'Low'


# High 그룹
ds.high <- ds.pure[ds.pure$group=='High',-24]
MYCOR(ds.high)

# Middle 그룹
ds.middle <- ds.pure[ds.pure$group=='Middle',-24]
MYCOR(ds.middle)

# Low 그룹
ds.low <- ds.pure[ds.pure$group=='Low',-24]
MYCOR(ds.low)

# 새로운 변수의 발굴 #########################

# 주택이 위치한 지역의 평균 집값을 새로운 변수로 생성
ds.pure$area.price <- NA
for(i in 1: nrow(ds)) {
  area <- ds[i,'zipcode']
  idx <- which(ds.agg$area==area)
  ds.pure$area.price[i] <- ds.agg[idx,'price']
}
cor(ds.pure$price, ds.pure$area.price)

# 주요 변수에 가중치 부여
imp.var <- c('sqft_living', 'grade', 'sqft_above', 'sqft_living15', 'bathrooms')

for (var in imp.var) {
  cat(var, 'normal :', cor(ds.pure$price, ds.pure[,var]), '\n')
  cat(var, 'weight :', cor(ds.pure$price, ds.pure[,var]^2), '\n')
}

