wt <- mtcars$wt                  # 중량 자료
mpg <- mtcars$mpg                # 연비 자료
plot(wt, mpg,                    # 2개 변수(x축, y축)
     main="중량-연비 그래프",    # 제목
     xlab="중량",                # x축 레이블
     ylab="연비(MPG)",           # y축 레이블
     col="red",                  # point의 color
     pch=19)                     # point의 종류
