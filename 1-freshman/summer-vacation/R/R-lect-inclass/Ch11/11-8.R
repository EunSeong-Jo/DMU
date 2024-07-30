test <- iris[,1:4]                  # 예측 대상 데이터 준비
pred <- predict(mod.iris, test)     # 모델을 이용한 예측
pred <- round(pred,0)
pred                                # 예측 결과 출력

answer <- as.integer(iris$Species)  # 실제 품종 정보
pred == answer                      # 예측 품종과 실제 품종이 같은지 비교
iris[pred != answer, ]              # 

acc <- mean(pred == answer)         # 예측 정확도 계산
acc                                 # 예측 정확도 출력

146 / 150
sum(pred == answer) / nrow(iris)
