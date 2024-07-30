par(mfrow=c(1,3))
barplot(table(mtcars$carb), 
        main="Barplot of Carburetors",
        xlab="#of carburetors",  
        ylab="frequency",
        col="blue")
barplot(table(mtcars$cyl), 
        main="Barplot of Cylender",
        xlab="#of cylender",  
        ylab="frequency",
        col="red")
barplot(table(mtcars$gear), 
        main="Barplot of Grar",
        xlab="#of gears",  
        ylab="frequency",
        col="green")
par(mfrow=c(1,1))
