x <- data.frame(name=c("a","b","c"), math=c(90,80,40))
y <- data.frame(sname=c("a","b","d"), korean=c(75,60,90))
x                         # 병합 기준 열의 이름이 name
y                         # 병합 기준 열의 이름이 sname

merge(x,y, by.x=c("name"), by.y=c("sname"))


merge(x,y, all.x = T, by.x=c("name"), by.y=c("sname"))
merge(x,y, all.y = T, by.x=c("name"), by.y=c("sname"))
merge(x,y, all = T, by.x=c("name"), by.y=c("sname"))
