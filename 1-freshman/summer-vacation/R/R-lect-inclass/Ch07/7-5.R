# 모든 셀에 대해 na 검사
is.na(x)

rowSums(is.na(x))         # 행별 NA의 개수
sum(rowSums(is.na(x)) > 0)  # NA가 포함된 행의 개수

sum(is.na(x))             # 데이터셋 전체에서 NA 개수
sum(rowSums(is.na(x)))    # 데이터셋 전체에서 NA 개수, 위 사용

# NA가 있는 행 출력
x[rowSums(is.na(x)) > 0, ]
subset(x, rowSums(is.na(x)) > 0)

# NA가 없는 행 출력
x[rowSums(is.na(x)) == 0, ]
subset(x, rowSums(is.na(x)) == 0)
