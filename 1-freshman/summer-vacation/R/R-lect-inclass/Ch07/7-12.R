subset(iris, Species == "setosa")
subset(iris, Sepal.Length > 7.5)
subset(iris, Sepal.Length > 5.1 & Sepal.Width > 3.9)

subset(iris, Sepal.Length > 7.6,
       select=c(Petal.Length,Petal.Width))
