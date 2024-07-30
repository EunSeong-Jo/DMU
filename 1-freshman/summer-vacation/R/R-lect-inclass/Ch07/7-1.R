z <- c(1,2,3,NA,5,NA,8)    # 결측값이 포함된 벡터 z
sum(z)                     # 정상 계산이 안 됨
is.na(z)                   # NA 여부 확인
sum(is.na(z))              # NA의 개수 확인
sum(z, na.rm=TRUE)         # NA를 제외하고 합계를 계산

z <- c(1,2,3,NA,5,NA,8, NaN)  # 결측값이 포함된 벡터 z
sum(z)                        # 정상 계산이 안 됨
is.na(z)                      # NA 여부 확인
sum(is.na(z))                 # NA의 개수 확인
sum(z, na.rm=TRUE)            # NA를 제외하고 합계를 계산
