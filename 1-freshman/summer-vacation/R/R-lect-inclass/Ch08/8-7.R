library(ggplot2)

ggplot(iris, aes(x=Petal.Length)) +    # 그래프를 그릴 데이터 지정
  geom_histogram(binwidth=0.5)         # 히스토그램 작성
