head(mtcars)
mosaicplot(~gear+vs, data = mtcars, color=TRUE, 
           main ="Gear and Vs")
mosaicplot(~gear+vs, data = mtcars, color=c("green","blue"),
           main ="Gear and Vs")

table(mtcars$gear, mtcars$vs)
table(mtcars$vs, mtcars$gear)
