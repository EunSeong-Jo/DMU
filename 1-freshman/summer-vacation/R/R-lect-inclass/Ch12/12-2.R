std <- function(X) {                # 표준화 함수
  return((X-min(X)) /(max(X)-min(X)))
}

mydata <- apply(iris[,1:4], 2, std)  # 표준화된 데이터 준비

fit <- kmeans(x=mydata, centers=3)
fit
