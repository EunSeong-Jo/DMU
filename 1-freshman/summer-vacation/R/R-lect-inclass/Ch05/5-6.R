mydata <- c(60, 62, 64, 65, 68, 69, 120)
quantile(mydata)
quantile(mydata, (0:10)/10)         # 10% 단위로 구간을 나누어 계산
summary(mydata)

mydata <- c(1, 2, 5, 3, 4)
quantile(mydata)
quantile(mydata, (0:10)/10)         # 10% 단위로 구간을 나누어 계산
summary(mydata)

mydata <- c(1, 2, 3, 4)
# median(50%): 2, 3의 평균값
# 25%(Q1): 1과 median()의 평균값, 간략 계산법
# 75%(Q3): median()과 4의 평균값, 간략 계산법
quantile(mydata)
quantile(mydata, (0:10)/10)         # 10% 단위로 구간을 나누어 계산
summary(mydata)

mydata <- c(14, 15, 16, 17, 21, 22, 30, 34, 39, 41, 45, 47)
quantile(mydata)
quantile(mydata, probs=.25, type=7)

quantile(mydata, (0:10)/10)         # 10% 단위로 구간을 나누어 계산
summary(mydata)
