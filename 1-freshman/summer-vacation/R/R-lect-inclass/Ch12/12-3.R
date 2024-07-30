install.packages("class")
library(class)

# 훈련용 데이터와 테스트용 데이터 준비
tr.idx <- c(1:25,51:75, 101:125)    # 훈련용 데이터의 인덱스
ds.tr <- iris[tr.idx, 1:4]          # 훈련용 데이터셋
ds.ts <- iris[-tr.idx, 1:4]         # 테스트용 데이터셋
cl.tr <- factor(iris[tr.idx, 5])    # 훈련용 데이터셋의 그룹(품종) 정보
cl.ts <- factor(iris[-tr.idx, 5])   # 테스트용 데이터셋의 그룹(품종) 정보

pred <- knn(ds.tr, ds.ts, cl.tr, k=3, prob=TRUE)
pred

acc <- mean(pred==cl.ts)            # 예측 정확도
acc

table(pred,cl.ts)                   # 예측값과 실제값 비교 통계
