# setwd("D:/source")    

write.csv(airquality, file="airquality.csv")

# 작업 폴더 지정
air <- read.csv("airquality.csv", header=T)   # .csv 파일 읽기
head(air)

air
