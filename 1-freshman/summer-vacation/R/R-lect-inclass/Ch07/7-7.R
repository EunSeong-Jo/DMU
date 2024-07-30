str(state.x77)
is.matrix(state.x77)
is.array(state.x77)
is.data.frame(state.x77)

st <- data.frame(state.x77)
str(st)

boxplot(st$Income)
boxplot.stats(st$Income)$out

quantile(st$Income, 0:3/4)
summary(st$Income)

boxplot.stats(st$Income)

boxplot.stats(st$Income)$stats
boxplot.stats(st$Income)$n
boxplot.stats(st$Income)$conf
boxplot.stats(st$Income)$out
