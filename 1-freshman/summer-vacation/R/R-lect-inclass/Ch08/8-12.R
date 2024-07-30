library(ggplot2)

ggplot(data=iris, aes(y=Petal.Length, fill=Species)) + 
  geom_boxplot() 


str(iris)
boxplot(iris$Petal.Length ~ iris$Species, iris, 
        col = c("lightgray", "yellow", "skyblue"))

        