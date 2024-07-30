# 상품 판매 빈도
itemFrequencyPlot(trans, topN=10, type="absolute", xlab="상품명", 
                  ylab="절대 판매빈도", main="판매량 많은 상품", col="green")
itemFrequencyPlot(trans, topN=10, type="relative", xlab="상품명", 
                  ylab="상대 판매빈도", main="판매량 많은 상품", col="blue")

# 연관규칙 찾기
rules <- apriori(trans, parameter = list(supp = 0.001, conf = 0.7))
rules

summary(rules)
# 앞쪽 10개의 규칙 출력 
options(digits=2)              # 평가척도 값의 자리수 지정         
inspect(rules[1:5])
options(digits=5)              # 평가척도 값의 자리수 지정         
inspect(rules[1:10])
inspect(rules)

# 향상도 순위 출력 
lift.sort <- sort(rules, by='lift', decreasing = T)
inspect(lift.sort)
# 지지도 순위 출력 
support.sort <- sort(rules, by='support', decreasing = T)
inspect(support.sort)

# 신뢰도 상위 10개 규칙 출력 
rules.sort <- sort(rules, by='confidence', decreasing = T)
inspect(rules.sort[1:10])

# 산점도 (지지도-향상도) 
plot(rules.sort, measure=c("support", "lift"), shading="confidence")
plot(rules.sort, measure=c("confidence", "lift"), shading="support")
plot(rules.sort, measure=c("confidence", "lift"), jitter=T, shading="support")

# Graph plot
plot(rules.sort, method="graph")

# Grouped Matrix Plot
plot(rules.sort, method="grouped")

## 연관규칙 저장
write(rules.sort, file="Ch10\\BreadBasket_rules.csv",
      sep=',', quote=T, row.names=F)

