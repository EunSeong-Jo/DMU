library(carData)
str(UN)
temp <- UN[,3:7]                     
temp <- temp[complete.cases(temp), ] 

temp <- scale(temp)

fit <- kmeans(temp, center=3)
grp <- fit$cluster
grp

agg <- aggregate(UN[complete.cases(UN),c('ppgdp','infantMortality')], 
                 by=list(grp=grp), mean)
agg$grp <- factor(agg$grp)
agg

library(ggplot2)
ggplot(agg, aes(x=grp,y=ppgdp)) +
  geom_bar(stat='identity', width=0.7, fill='steelblue') + 
  ggtitle('그룹별 1인당국내총생산')
ggplot(agg, aes(x=grp,y=infantMortality)) +
  geom_bar(stat='identity', width=0.7, fill='orange') + 
  ggtitle('그룹별 영아사망률')
