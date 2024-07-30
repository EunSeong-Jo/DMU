library(mlbench)
data(Vehicle)

head(Vehicle)

agg <- aggregate(Vehicle[,'Max.L.Ra'], by=list(차량타입=Vehicle$Class),
                 FUN=mean)
agg

barplot(agg$x, names.arg=agg$차량타입, main='차량유형별 종횡비')
