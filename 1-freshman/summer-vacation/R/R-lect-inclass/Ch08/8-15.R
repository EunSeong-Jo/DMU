install.packages(c("rgl", "car"))

library("car")
library("rgl")
library("mgcv")
library(Rtsne)

tsne <- Rtsne(ds, dims=3, perplexity=10)
df.tsne <- data.frame(tsne$Y)
head(df.tsne)

# 회귀면이 포함된 3차원 산점도
scatter3d(x=df.tsne$X1, y=df.tsne$X2, z=df.tsne$X3)

# 회귀면이 없는 3차원 산점도
points <- as.integer(ds.y)
points
color <- c('red','green','blue')
scatter3d(x=df.tsne$X1, y=df.tsne$X2, z=df.tsne$X3,
          point.col = color[points],    # 점의 색을 품종별로 다르게
          surface=FALSE)                # 회귀면을 표시하지 않음

scatter3d(x=df.tsne$X1, y=df.tsne$X2, z=df.tsne$X3,
          point.col = color[points],    # 점의 색을 품종별로 다르게
          surface=T)                # 회귀면을 표시하지 않음
