# 이전 메모리 제거
rm(list = ls())

# code 7-7
str(state.x77)
is.matrix(state.x77)
is.array(state.x77)
is.data.frame(state.x77)

st <- data.frame(state.x77)
str(st)
colnames(st)

boxplot(st$Income)
boxplot.stats(st$Income)$out
boxplot(st$Income)$out

out.box <- boxplot(st$Income)
out.box
is.list(out.box)

quantile(st$Income, 0:3/4)
round(quantile(st$Income, 0:3/4))
summary(st$Income)

boxplot.stats(st$Income)

boxplot.stats(st$Income)$stats
boxplot.stats(st$Income)$n
boxplot.stats(st$Income)$conf # 신뢰구간 95% 내의 범위
boxplot.stats(st$Income)$out

#############################################
boxplot(st$Income)$stats
boxplot(st$Income)$n
boxplot(st$Income)$conf
boxplot(st$Income)$out
#############################################

# code 7-8
out.val <- boxplot.stats(st$Income)$out    # 특이값 추출
st$Income[st$Income %in% out.val] <- NA    # 특이값을 NA로 대체
head(st)
newdata <- st[complete.cases(st),]         # NA가 포함된 행 제거
head(newdata)

#############################################
out.val <- boxplot(st$Income)$out    # 특이값 추출
st$Income[st$Income %in% out.val] <- NA    # 특이값을 NA로 대체
head(st)
newdata <- st[complete.cases(st),]         # NA가 포함된 행 제거
head(newdata)
