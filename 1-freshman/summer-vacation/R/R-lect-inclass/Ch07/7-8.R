out.val <- boxplot.stats(st$Income)$out    # 특이값 추출
st$Income[st$Income %in% out.val] <- NA    # 특이값을 NA로 대체
head(st)
newdata <- st[complete.cases(st),]         # NA가 포함된 행 제거
head(newdata)
