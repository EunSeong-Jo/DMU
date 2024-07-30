library(MASS)                           # stepAIC() 함수 제공
newdata2 <- Prestige[,c(1:5)]           # 모델 구축에 사용할 데이터셋 생성
head(newdata2)
mod2 <- lm(income ~ education + prestige + women + census, 
           data= newdata2)

summary(mod2)

mod2 <- lm(income ~ ., 
           data= newdata2)

summary(mod2)


mod3 <- stepAIC(mod2)                   # 변수 선택 진행
mod3                                    # 변수 선택 후 결과 확인

summary(mod3)                           # 회귀모델 상세 내용 확인
