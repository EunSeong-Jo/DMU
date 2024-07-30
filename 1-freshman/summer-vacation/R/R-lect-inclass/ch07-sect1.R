# 이전 메모리 제거
rm(list = ls())

# code 7-1
z <- c(1,2,3,NA,5,NA,8)    # 결측값이 포함된 벡터 z
sum(z)                     # 정상 계산이 안 됨
mean(z)                    # 정상 계산이 안 됨
median(z)
is.na(z)                   # NA 여부 확인
sum(is.na(z))              # NA의 개수 확인
sum(z, na.rm=TRUE)         # NA를 제외하고 합계를 계산

z <- c(1,2,3,NA,5,NA,8, NaN)  # 결측값이 포함된 벡터 z
sum(z)                        # 정상 계산이 안 됨
is.na(z)                      # NA 여부 확인
sum(is.na(z))                 # NA의 개수 확인
sum(z, na.rm=TRUE)            # NA를 제외하고 합계를 계산

# code 7-2
z1 <- c(1,2,3,NA,5,NA,8)     # 결측값이 포함된 벡터 z1
z2 <- c(5,8,1,NA,3,NA,7)     # 결측값이 포함된 벡터 z2
z1[is.na(z1)] <- 0           # NA를 0으로 치환
z1
z3 <- as.vector(na.omit(z2)) # NA를 제거하고 새로운 벡터 생성
z3

z3 <- c(1,2,3,NA,5,NA,8)     # 결측값이 포함된 벡터 z1
na.omit(z3)
z3

z3[is.na(z3)] <- mean(z3, na.rm=T)  # NA를 평균으로 치환
z3

# code 7-3
# NA를 포함하는 test 데이터 생성
x <- iris
x[1,2]<- NA; x[1,3]<- NA
x[2,3]<- NA; x[3,4]<- NA  
head(x)

# code 7-4
x <- iris
x[1,2]<- NA; x[1,3]<- NA
x[2,3]<- NA; x[3,4]<- NA  
head(x)

is.na(x[,1])

# for문을 이용한 방법
for (i in 1:ncol(x)) {
  this.na <- is.na(x[,i]) 
  cat(colnames(x)[i], "\t", sum(this.na), "\n")
}

# apply를 이용한 방법
col_na <- function(y) {
  return(sum(is.na(y)))
}

na_count <-apply(x, 2, FUN=col_na)
na_count

#############################################
# 익명함수 사용
na_count <- apply(x, 2, FUN = function(x) sum(is.na(x)))
na_count
# NA가 있는 열만 출력
na_count[na_count>0]

# airquality
colnames(airquality)
na.cnt <- apply(airquality, 2, FUN = function(x) sum(is.na(x)))
na.cnt[na.cnt > 0]
#############################################

# code 7-5
# 모든 셀에 대해 na 검사
is.na(x)

rowSums(is.na(x))         # 행별 NA의 개수
sum(rowSums(is.na(x)) > 0)  # NA가 포함된 행의 개수

sum(is.na(x))             # 데이터셋 전체에서 NA 개수
sum(rowSums(is.na(x)))    # 데이터셋 전체에서 NA 개수, 위 사용

# NA가 있는 행 출력
x[rowSums(is.na(x)) > 0, ]
subset(x, rowSums(is.na(x)) > 0)

#############################################
# airquality
colnames(airquality)
rowSums(is.na(airquality))
colSums(is.na(airquality))

# NA가 있는 행
airquality[rowSums(is.na(airquality)) > 0, ]
subset(airquality, rowSums(is.na(airquality)) > 0)
#############################################

# code 7-6
head(x)
x[!complete.cases(x),]         # NA가 포함된 행들 출력
y <- x[complete.cases(x),]     # NA가 포함된 행들 제거
head(y)    

#############################################
# airquality
head(airquality)
airquality[!complete.cases(airquality), ]
head(airquality[complete.cases(airquality),])
#############################################