tmp <- airquality[,1:4]

tmp <- tmp[complete.cases(tmp),]

head(tmp)
plot(tmp)
cor(tmp)

cor(tmp$Ozone, tmp$Temp)
plot(tmp$Ozone, tmp$Temp, main="오존-온도")
