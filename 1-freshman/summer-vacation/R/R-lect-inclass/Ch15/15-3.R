MAE <- function(pred, answer) {
  return (mean(abs(pred-answer)))
}

# 기본 모델의 개발과 평가
myds <- ds[,-c(1,2, 17)]
model.base <- lm(price~., data=myds)
summary(model.base)

myds <- ds[,-c(1,2, 14, 17)]

# 기본 모델 예측 성능 평가
set.seed(1234)
ts.idx <- sample(nrow(myds), nrow(myds)*.3) 

model.base <- lm(price~., data=myds[-ts.idx,])
pred <- predict(model.base, myds[ts.idx,])
MAE(pred, myds$price[ts.idx])

# 지역평균집값 포함 & 주요 변수 가중치 부여
myds$area.price <- NA
for(i in 1: nrow(ds)) {
  area <- ds[i,'zipcode']
  idx <- which(ds.agg$area==area)
  myds$area.price[i] <- ds.agg[idx,'price']
}

imp.var <- c('sqft_living', 'grade', 'sqft_above', 'sqft_living15', 'bathrooms')
for(var in imp.var) {
  myds[,var] <- myds[,var]^2 
}

model.1 <- lm(price~., data=myds[-ts.idx,])
pred <- predict(model.1, myds[ts.idx, ])
MAE(pred, myds$price[ts.idx])

# 변수 선택 시도
library(MASS)
model.2 <- stepAIC(model.1) 

# 주택을 클러스터링하여 3개 그룹으로 나눈 뒤 각각 모델 개발

# 클러스터링을 위한 데이터 스케일링
myds[,-1] <- scale(myds[,-1])

myds.tr <- myds[-ts.idx,]
myds.ts <- myds[ts.idx,]

# 클러스터링
result <- kmeans(myds.tr[,-1], centers=3)

myds.1 <- myds.tr[result$cluster==1,]
myds.2 <- myds.tr[result$cluster==2,]
myds.3 <- myds.tr[result$cluster==3,]

model.3.1 <- lm(price~., data=,myds.1)
model.3.2 <- lm(price~., data=,myds.2)
model.3.3 <- lm(price~., data=,myds.3)

# 테스트 데이터의 클러스터 결정
# install.packages("flexclust")
# install.packages("fdm2id")
library(flexclust)
library(fdm2id)
cl.ts <- predict(result, myds.ts[,-1])
pred <- NA
for (i in 1: nrow(myds.ts)) {
  if (cl.ts[i] == 1) {
    pred[i] <- predict(model.3.1, myds.ts[i,-1])
  } else if (cl.ts[i] == 2) {  
    pred[i] <- predict(model.3.2, myds.ts[i,-1])
  } else {
    pred[i] <- predict(model.3.3, myds.ts[i,-1])
  }   
}

MAE(pred, myds.ts$price)
