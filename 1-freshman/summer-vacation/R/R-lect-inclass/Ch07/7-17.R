# 열이름을 지정하지 않으면 Group.1 열 이름
# 품종에 따라 모든 변수(열)의 평균 구하기
agg <- aggregate(iris[,-5], by=list(iris$Species), 
                 FUN=mean)
agg

# 열 이름: 품종
# 품종에 따라 모든 변수(열)의 평균 구하기
agg <- aggregate(iris[,-5], by=list(품종 = iris$Species), 
                 FUN=mean)
agg

# 열 이름: 품종
# 품종에 따라 모든 변수(열)의 중앙값 구하기
agg <- aggregate(iris[,-5], by=list(품종 = iris$Species), 
                 FUN=median)
agg
