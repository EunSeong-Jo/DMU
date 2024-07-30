# 이전 메모리 제거
rm(list = ls())

# code 3-10
dim(iris)       # 행과 열의 개수 출력
nrow(iris)      # 행의 개수 출력
ncol(iris)      # 열의 개수 출력
colnames(iris)  # 열 이름 출력, names()와 결과 동일
head(iris)      # 데이터셋의 앞부분 일부 출력
tail(iris)      # 데이터셋의 뒷부분 일부 출력

# code 3-11
str(iris)                 # 데이터셋 요약 정보 보기
iris[,5]                  # 품종 데이터 보기
unique(iris[,5])          # 품종의 종류 보기(중복 제거)
table(iris[,"Species"])   # 품종의 종류별 행의 개수 세기

# code 3-12
colSums(iris[,-5])    # 열별 합계
colMeans(iris[,-5])   # 열별 평균
rowSums(iris[,-5])    # 행별 합계
rowMeans(iris[,-5])   # 행별 평균

# code 3-13
z <- matrix(1:20, nrow=4, ncol=5)
z
t(z)   # 행과 열 방향 전환

# code 3-14
IR.1 <- subset(iris, Species=="setosa")
IR.1
IR.2 <- subset(iris, Sepal.Length>5.0 &
                 Sepal.Width>4.0)
IR.2
IR.2[, c(2,4)]                  # 2, 4열의 값만 추출

# code 3-15
a <- matrix(1:20,4,5)
b <- matrix(21:40,4,5)
a
b

2*a                 # 매트릭스 a에 저장된 값들에 2를 곱하기
b-5
2*a + 3*b

a+b
b-a
b/a
a*b

a <- a*3
b <- b-5

# code 3-16
class(iris)             # iris 데이터셋의 자료구조 확인
class(state.x77)        # state.x77 데이터셋의 자료구조 확인
is.matrix(iris)         # 데이터셋이 매트릭스인지를 확인하는 함수
is.data.frame(iris)     # 데이터셋이 데이터프레임인지를 확인하는 함수

state.x77
state.x77['Alaska', 'Income']
is.matrix(state.x77)
is.data.frame(state.x77)

#################################################
state.region
is.factor(state.region)

str(state.region)
levels(state.region)

is.factor(state.region)
is.vector(state.region)
is.matrix(state.region)
is.data.frame(state.region)
#################################################

# code 3-17
# 매트릭스를 데이터프레임으로 변환
st <- data.frame(state.x77)
head(st)
class(st)

# 데이터프레임을 매트릭스로 변환
iris.m <- as.matrix(iris[,1:4])
head(iris.m)
class(iris.m)

# code 3-18
iris[,"Species"]  # 결과=벡터. 매트릭스와 데이터프레임 모두 가능
iris[,5]          # 결과=벡터. 매트릭스와 데이터프레임 모두 가능
iris["Species"]   # 결과=데이터프레임. 데이터프레임만 가능
iris[5]           # 결과=데이터프레임. 데이터프레임만 가능
iris$Species      # 결과=벡터. 데이터프레임만 가능
is.factor(iris$Species)      # 결과=벡터. 데이터프레임만 가능
is.vector(c(1, 2))

