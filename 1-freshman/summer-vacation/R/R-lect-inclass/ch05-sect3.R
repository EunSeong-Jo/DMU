# 메모리 제거 
rm(list = ls())

# code 5-05
weight <- c(60, 62, 64, 65, 68, 69)
weight.heavy <- c(weight, 120)
weight
weight.heavy

mean(weight)                    # 평균
mean(weight.heavy)              # 평균

median(weight)                  # 중앙값
median(weight.heavy)            # 중앙값

mean(weight, trim=0.2)          # 절사평균(상하위 20% 제외)
mean(weight.heavy,trim=0.2)     # 절사평균(상하위 20% 제외)

# code 5-06
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

# code 5-07
mydata <- c(60, 62, 64, 65, 68, 69, 120)
var(mydata)           # 분산, 평균에서 떨어진 정도
sd(mydata)            # 표준편차
range(mydata)         # 값의 범위

diff(range(mydata))   # 최댓값, 최솟값의 차이??
diff(c(150, 22))
diff(c(10, 100))

# code 5-08
str(cars)
head(cars)

dist <- cars[,2]                      # 자동차 제동거리
hist(dist,                            # 자료(data)
     main="Histogram for 제동거리",   # 제목
     xlab ="제동거리",                # x축 레이블
     ylab="빈도수",                   # y축 레이블
     border="blue",                   # 막대 테두리색
     col="green",                     # 막대 색
     las=2,                           # x축 글씨 방향(0~3)
     breaks=2)                        # 막대 개수 조절

hist(dist,                            # 자료(data)
     main="Histogram for 제동거리",   # 제목
     xlab ="제동거리",                # x축 레이블
     ylab="빈도수",                   # y축 레이블
     border="blue",                   # 막대 테두리색
     col="green",                     # 막대 색
     las=2,                           # x축 글씨 방향(0~3)
     breaks=3)                        # 막대 개수 조절

hist(dist,                            # 자료(data)
     main="Histogram for 제동거리",   # 제목
     xlab ="제동거리",                # x축 레이블
     ylab="빈도수",                   # y축 레이블
     border="blue",                   # 막대 테두리색
     col="green",                     # 막대 색
     las=2,                           # x축 글씨 방향(0~3)
     breaks=4)                        # 막대 개수 조절

hist(dist,                            # 자료(data)
     main="Histogram for 제동거리",   # 제목
     xlab ="제동거리",                # x축 레이블
     ylab="빈도수",                   # y축 레이블
     border="blue",                   # 막대 테두리색
     col="green",                     # 막대 색
     las=2,                           # x축 글씨 방향(0~3)
     breaks=5)                        # 막대 개수 조절

# code 5-09
dist <- cars[,2]    # 자동차 제동거리(단위: 피트)
boxplot(dist, main="자동차 제동거리")

# code 5-10
boxplot.stats(dist)

boxplot.stats(dist)$stats
# $stats
# c이 값은 박스 플롯의 주요 통계치를 나타내며, 
# 다섯 개의 숫자 요약 (Five Number Summary)이라고 불립니다. 
# 각각의 값은 다음을 의미합니다:
#   
# 정상범위 내에서의 최소값 (Minimum): 2
# 1사분위수 (Q1, 25th Percentile): 26
# 중앙값 (Median, 50th Percentile): 36
# 3사분위수 (Q3, 75th Percentile): 56
# 정상범위 내에서의 최대값 (Maximum): 93

boxplot.stats(dist)$conf
# $conf
# 이 값은 중앙값의 신뢰 구간(Confidence Interval)을 나타냅니다.
# 신뢰 구간은 중앙값의 추정치가 어느 범위에 위치할 것인지 나타내며, 
# 보통 95% 신뢰 구간을 계산합니다.
# 
# 하한 (Lower Bound): 29.29663
# 상한 (Upper Bound): 42.70337
# 이 값들은 중앙값이 해당 범위 내에 있을 것이라는 것을 나타냅니다.

# code 5-11
boxplot(Petal.Length~Species, data=iris, main="품종별 꽃잎의 길이")

boxplot(Petal.Width~Species, data=iris, main="품종별 꽃잎의 너비")

# stop 201
par(mfrow=c(1,3))
barplot(table(mtcars$carb), 
        main="Barplot of Carburetors",
        xlab="#of carburetors",  
        ylab="frequency",
        col="blue")
barplot(table(mtcars$cyl), 
        main="Barplot of Cylender",
        xlab="#of cylender",  
        ylab="frequency",
        col="red")
barplot(table(mtcars$gear), 
        main="Barplot of Grar",
        xlab="#of gears",  
        ylab="frequency",
        col="green")
par(mfrow=c(1,1)) # 해제




