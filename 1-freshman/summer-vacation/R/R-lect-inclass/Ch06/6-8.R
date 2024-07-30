## (1) Prepare Data ----------------------
if (!require("mlbench")) {
  install.packages("mlbench")
}
library(mlbench)

data("BostonHousing")
colnames(BostonHousing)

myds <- BostonHousing[,c("crim","rm","dis","tax","medv")]

## (2) Add new column ----------------------
grp <- c()
for (i in 1:nrow(myds)) {                    # myds$medv 값에 따라 그룹 분류
  if (myds$medv[i] >= 25.0) {
    grp[i] <- "H"
  } else if (myds$medv[i] <= 17.0) {
    grp[i] <- "L"
  } else {
    grp[i] <- "M"
  }
}
grp <- factor(grp)                           # 문자벡터를 팩터 타입으로 변경
grp <- factor(grp, levels=c("H","M","L"))    # 레벨의 순서를 H,L,M -> H,M,L

myds <- data.frame(myds, grp)                # myds에 grp 컬럼 추가

## (3) Add new column ----------------------
str(myds)
head(myds)
table(myds$grp)                              # 주택 가격 그룹별 분포

## (4) histogram ----------------------
par(mfrow=c(2,3))                            # 2x3 가상화면 분할
for(i in 1:5) {
  hist(myds[,i], main=colnames(myds)[i], col="yellow")
}
par(mfrow=c(1,1))                            # 2x3 가상화면 분할 해제

## (5) boxplot ----------------------
par(mfrow=c(2,3))                            # 2x3 가상화면 분할
for(i in 1:5) {
  boxplot(myds[,i], main=colnames(myds)[i])
}
par(mfrow=c(1,1))                            # 2x3 가상화면 분할 해제

## (6) boxplot by group ------------------
boxplot(myds$crim ~ myds$grp, main="1인당 범죄율")
boxplot(myds$rm ~ myds$grp, main="방의 수")
boxplot(myds$dis ~ myds$grp, main="직업센터까지의 거리")
boxplot(myds$tax ~ myds$grp, main="재산세")

## (7) scatter plot ------------------
pairs(myds[,-6])

## (8) scatter plot with group ------------------
point <- as.integer(myds$grp)                # 점의 모양 지정
color <- c("red","green","blue")             # 점의 색 지정
pairs(myds[,-6], pch=point, col=color[point])

## (9) correlation coefficient ------------------
cor(myds[,-6])
