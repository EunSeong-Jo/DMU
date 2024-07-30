month = 1:12
late1 = c(5,8,7,9,4,6,12,13,8,6,6,4)
late2 = c(4,6,5,8,7,8,10,11,6,5,7,3)
plot(month,                          # x data
     late1,                          # y data
     main="Late Students",
     type= "b",                      # 그래프의 종류 선택(알파벳)
     lty=1,                          # 선의 종류(line type) 선택
     col="red",                      # 선의 색 선택
     xlab="Month ",                  # x축 레이블
     ylab="Late cnt",                # y축 레이블
     ylim=c(1, 15)                   # y축 값의 (하한, 상한)
)
lines(month,                         # x data
      late2,                         # y data
      type = "b",                    # 선의 종류(line type) 선택
      col = "blue")                  # 선의 색 선택
