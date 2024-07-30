month = 1:12                          # 자료 입력
late = c(5,8,7,9,4,6,12,13,8,6,6,4)   # 자료 입력
plot(month,                           # x data
     late,                            # y data
     main="지각생 통계",              # 제목
     type= "l",                       # 그래프의 종류 선택(알파벳)
     lty=1,                           # 선의 종류(line type) 선택
     lwd=1,                           # 선의 굵기 선택
     xlab="Month",                    # x축 레이블
     ylab="Late cnt"                  # y축 레이블
)
