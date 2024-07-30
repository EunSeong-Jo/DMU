speed <- cars[,1]                   # 주행속도
pred <- W * speed + b
pred                                # 예상 제동거리

compare <- data.frame(pred, cars[,2], pred-cars[,2])
colnames(compare) <- c('예상','실제','오차')
head(compare)
