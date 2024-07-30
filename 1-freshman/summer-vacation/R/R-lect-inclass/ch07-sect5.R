# 이전 메모리 제거
rm(list = ls())

# code 7-13
x <- 1:100
y <- sample(x, size=10, replace = FALSE)  # 비복원추출
y

# code 7-14
idx <- sample(1:nrow(iris), size=50, replace = FALSE)
iris.50 <- iris[idx,]               # 50개의 행 추출
dim(iris.50)                        # 행과 열의 개수 확인
head(iris.50)
View(iris.50)

# code 7-15
sample(1:20, size=5)
sample(1:20, size=5)
sample(1:20, size=5)

set.seed(100)
sample(1:20, size=5)
set.seed(100)
sample(1:20, size=5)
set.seed(100)
sample(1:20, size=5)

set.seed(100)
sample(1:4, size=5) # 오류
sample(1:4, size=5, replace=T)

##############################################
if (!require(dplyr)) {
  install.packages("dplyr")
}
library(dplyr)
sample_n(iris, 10)     # 10개
sample_frac(iris)      # 전체
sample_frac(iris, .1)  # 10%
##############################################

# code 7-16
combn(1:5,3)                      # 1~5에서 3개를 뽑는 조합

x = c("red","green","blue","black","white")
com <- combn(x, 2)                 # x의 원소를 2개씩 뽑는 조합
com
is.matrix(com)
ncol(com) # 10

for(i in 1:ncol(com)) {           # 조합을 출력
  cat(com[,i], "\n")
}
