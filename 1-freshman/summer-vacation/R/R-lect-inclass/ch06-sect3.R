# 이전 메모리 제거
rm(list = ls())

# code 6-6
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

# code 6-7
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

# 위 그림에 다음 그림을 그림
lines(month,                         # x data
      late2,                         # y data
      type = "b",                    # 선의 종류(line type) 선택
      col = "blue")                  # 선의 색 선택

