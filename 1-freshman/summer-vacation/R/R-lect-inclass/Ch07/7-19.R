head(mtcars)
agg <- aggregate(mtcars, by=list(cyl=mtcars$cyl, vs=mtcars$vs), FUN=max)
agg
