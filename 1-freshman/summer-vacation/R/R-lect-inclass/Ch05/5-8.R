str(cars)
head(cars)

dist <- cars[,2]                      # 자동차 제동거리
hist(dist,                            # 자료(data)
     main="Histogram for 제동거리",   # 제목
     xlab ="제동거리",                # x축 레이블
     ylab="빈도수",                   # y축 레이블
     border="blue",                   # 막대 테두리색
     col="green",                     # 막대 색
     las=2,                           # x축 글씨 방향(0~3)
     breaks=2)                        # 막대 개수 조절

hist(dist,                            # 자료(data)
     main="Histogram for 제동거리",   # 제목
     xlab ="제동거리",                # x축 레이블
     ylab="빈도수",                   # y축 레이블
     border="blue",                   # 막대 테두리색
     col="green",                     # 막대 색
     las=2,                           # x축 글씨 방향(0~3)
     breaks=3)                        # 막대 개수 조절

hist(dist,                            # 자료(data)
     main="Histogram for 제동거리",   # 제목
     xlab ="제동거리",                # x축 레이블
     ylab="빈도수",                   # y축 레이블
     border="blue",                   # 막대 테두리색
     col="green",                     # 막대 색
     las=2,                           # x축 글씨 방향(0~3)
     breaks=4)                        # 막대 개수 조절

hist(dist,                            # 자료(data)
     main="Histogram for 제동거리",   # 제목
     xlab ="제동거리",                # x축 레이블
     ylab="빈도수",                   # y축 레이블
     border="blue",                   # 막대 테두리색
     col="green",                     # 막대 색
     las=2,                           # x축 글씨 방향(0~3)
     breaks=5)                        # 막대 개수 조절
