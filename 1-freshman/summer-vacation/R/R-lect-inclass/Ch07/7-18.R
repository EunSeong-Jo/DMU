agg <- aggregate(iris[,-5], by=list(표준편차=iris$Species),
                 FUN=sd)
agg
