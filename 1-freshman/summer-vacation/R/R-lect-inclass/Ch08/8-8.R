library(ggplot2)

ggplot(iris, aes(x=Sepal.Width, fill=Species, color=Species)) + 
  geom_histogram(binwidth = 0.5, position="dodge") + 
  theme(legend.position="top")

ggplot(iris, aes(x=Sepal.Width, fill=Species, color=Species)) + 
  geom_histogram(binwidth = 0.5, position="dodge") + 
  theme(legend.position="left")
