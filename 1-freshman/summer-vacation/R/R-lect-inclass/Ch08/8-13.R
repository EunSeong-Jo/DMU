library(ggplot2)

airmiles
year <- 1937:1960
cnt <- as.vector(airmiles)
df <- data.frame(year,cnt)             # 데이터 준비
head(df)

ggplot(data=df, aes(x=year,y=cnt)) +   # 선그래프 작성
  geom_line(col="red")

plot(airmiles)
