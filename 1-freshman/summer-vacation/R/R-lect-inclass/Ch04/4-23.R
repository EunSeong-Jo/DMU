idx <- which(iris$Petal.Length > 5.0) # 꽃잎의 길이가 5.0 이상인 값들의 인덱스
idx
iris.big <- iris[idx,]              # 인덱스에 해당하는 값만 추출하여 저장
iris.big

str(iris.big)
