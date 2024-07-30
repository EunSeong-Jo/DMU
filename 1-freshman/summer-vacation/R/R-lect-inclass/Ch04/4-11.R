norow <- nrow(iris)                             # iris의 행의 수
mylabel <- c()                                  # 비어있는 벡터 선언

for(i in 1:norow) {
  if (iris$Petal.Length[i] <= 1.6) {            # 꽃잎의 길이에 따라 레이블 결정
    mylabel[i] <- 'L'
  } else if (iris$Petal.Length[i] >= 5.1) {
    mylabel[i] <- 'H'
  } else {
    mylabel[i] <- 'M'
  }
}
print(mylabel)                                  # 레이블 출력
newds <- data.frame(iris$Petal.Length, mylabel) # 꽃잎의 길이와 레이블 결합
head(newds)                                     # 새로운 데이터셋 내용 출력
