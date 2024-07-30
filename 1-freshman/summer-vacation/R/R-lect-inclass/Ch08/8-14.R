install.packages("Rtsne")
library(Rtsne)

library(ggplot2)

ds <- iris[,-5]             # 품종 정보 제외
ds
str(ds)

## 동일행: 102, 143 행
iris[102, ]
iris[143, ]

## 중복 데이터 제거
dup = which(duplicated(ds))
dup                         # 143번째 행 중복

ds <- ds[-dup,]
str(ds)

ds.y <- iris$Species[-dup]  # 중복을 제외한 품종 정보
str(ds.y)
length(ds.y)

## t-SNE 실행
tsne <- Rtsne(ds, dims=2, perplexity=10)
tsne

tsne$Y

## 축소결과 시각화
df.tsne <- data.frame(tsne$Y)
head(df.tsne)

ggplot(df.tsne, aes(x=X1, y=X2, color=ds.y)) +
  geom_point(size=2)
