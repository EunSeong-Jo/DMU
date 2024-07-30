if (!require("car")) {
  install.packages("car")
}
  
library(car)
head(Prestige)

newdata <- Prestige[,c(1:4)]        # 회귀식 작성을 위한 데이터 준비
plot(newdata, pch=16, col="blue",   # 산점도를 통해 변수 간 관계 확인
     main="Matrix Scatterplot")
mod1 <- lm(income ~ education + prestige + women, # 회귀식 도출
           data=newdata)
summary(mod1)
