# 이전 메모리 제거
rm(list = ls())

# code 3-8
city <- c("Seoul","Tokyo","Washington")   # 문자로 이루어진 벡터
rank <- c(1,3,2)                          # 숫자로 이루어진 벡터
city.info <- data.frame(city, rank)       # 데이터프레임 생성
city.info  

# code 3-9
iris[,c(1:2)]                         # 1~2열의 모든 데이터
iris[,c(1,3,5)]                       # 1, 3, 5열의 모든 데이터
iris[,c("Sepal.Length","Species")]    # 1, 5열의 모든 데이터
iris[1:5,]                            # 1~5행의 모든 데이터
iris[1:5,c(1,3)]                      # 1~5행의 데이터 중 1, 3열의 데이터

