library(car)
tmp <- SLID[complete.cases(SLID),]

tmp$group <- 'Middle'
tmp$group[tmp$education>=14] <- 'High'
tmp$group[tmp$education<10] <- 'Low'

tmp$group <- factor(tmp$group, levels = c('High', 'Middle', 'Low'))

library(ggplot2)
ggplot(data=tmp, aes(y=wages, fill=group)) +
  geom_boxplot()
