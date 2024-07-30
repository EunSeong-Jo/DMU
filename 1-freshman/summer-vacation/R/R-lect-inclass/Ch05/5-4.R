favorite.color <- c(2, 3, 2, 1, 1, 2, 2, 1, 3, 2, 1, 3, 2, 1, 2)
ds <- table(favorite.color)
ds

barplot(ds, main='favorite color')
colors <- c('green', 'red', 'blue')
names(ds) <- colors         # 자료값 1,2,3을 green, red, blue로 변경
ds
barplot(ds, main='favorite color', col=colors)  # 색 지정 막대그래프
pie(ds, main='favorite color', col=colors)      # 색 지정 원그래프
