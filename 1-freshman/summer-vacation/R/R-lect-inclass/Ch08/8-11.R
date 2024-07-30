library(ggplot2)

ggplot(data=iris, aes(y=Petal.Length)) + 
  geom_boxplot(fill="yellow") 
