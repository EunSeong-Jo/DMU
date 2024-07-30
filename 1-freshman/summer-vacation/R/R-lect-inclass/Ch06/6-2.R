vars <- c("mpg","disp","drat","wt")    # 대상 변수
target <- mtcars[,vars]
head(target)
pairs(target,                          # 대상 데이터
      main="Multi Plots")
