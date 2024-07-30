z1 <- c(1,2,3,NA,5,NA,8)     # 결측값이 포함된 벡터 z1
z2 <- c(5,8,1,NA,3,NA,7)     # 결측값이 포함된 벡터 z2
z1[is.na(z1)] <- 0           # NA를 0으로 치환
z1
z3 <- as.vector(na.omit(z2)) # NA를 제거하고 새로운 벡터 생성
z3

z3 <- c(1,2,3,NA,5,NA,8)     # 결측값이 포함된 벡터 z1
z3[is.na(z3)] <- mean(z3, na.rm=T)  # NA를 평균으로 치환
z3


