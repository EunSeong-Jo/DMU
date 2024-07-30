# 이전 메모리 제거
rm(list = ls())

# code 7-9
v1 <- c(1,7,6,8,4,2,3)

order(v1)
# 결과: 값이 오름차순이 되는 첨자 번호
# [1] 1 6 7 5 3 2 4
paste(v1[1], v1[6], v1[7], v1[5], v1[3], v1[2], v1[4])

v1 <- sort(v1)                  # 오름차순
v1
v2 <- sort(v1, decreasing=T)    # 내림차순 
v2

# code 7-10
head(iris)
order(iris$Sepal.Length)

range(iris$Sepal.Length)
# 꽃받임 길이가 제일 작은 것 
iris[order(iris$Sepal.Length)[1], ]
# 꽃받임 길이가 제일 긴 것 
iris[order(iris$Sepal.Length)[nrow(iris)], ]

iris[order(iris$Sepal.Length),]               # 오름차순으로 정렬
iris[order(iris$Sepal.Length, decreasing=T),] # 내림차순으로 정렬
iris.new <- iris[order(iris$Sepal.Length),]   # 정렬된 데이터를 저장
head(iris.new)

# 정렬 기준이 2개
iris[order(iris$Species, -iris$Petal.Length, decreasing=T),] 

