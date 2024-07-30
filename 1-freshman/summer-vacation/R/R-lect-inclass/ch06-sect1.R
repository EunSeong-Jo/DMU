# 이전 메모리 제거
rm(list = ls())

# code 6-1
wt <- mtcars$wt                  # 중량 자료
mpg <- mtcars$mpg                # 연비 자료
plot(wt, mpg,                    # 2개 변수(x축, y축)
     main="중량-연비 그래프",    # 제목
     xlab="중량",                # x축 레이블
     ylab="연비(MPG)",           # y축 레이블
     col="red",                  # point의 color
     pch=19)                     # point의 종류

# code 6-2
# drat: 후방 차축비(rear axle ratio)
vars <- c("mpg","disp","drat","wt")    # 대상 변수
target <- mtcars[,vars]
head(target)
pairs(target,                          # 대상 데이터
      main="Multi Plots")

# code 6-3
iris.2 <- iris[,3:4]                   # 데이터 준비
point <- as.numeric(iris$Species)      # 점의 모양
point                                  # point 내용 출력
color <- c("red","green","blue")       # 점의 컬러
plot(iris.2,
     main="Iris plot",
     pch=c(point),
     col=color[point])

