install.packages("cvTools")
library(cvTools)                     # cvFolds() 함수 지원

k = 10                               # 10-fold
folds <- cvFolds(nrow(iris), K=k)    # 폴드 생성

acc <- c()                           # 폴드별 예측 정확도 저장용 벡터
for (i in 1:k) {
  ts.idx <- folds$which == i         # 테스트용 데이터의 인덱스
  ds.tr <- iris[-ts.idx, 1:4]        # 훈련용 데이터셋
  ds.ts <- iris[ts.idx, 1:4]         # 테스트용 데이터셋
  cl.tr <- factor(iris[-ts.idx, 5])  # 훈련용 데이터셋의 그룹(품종) 정보
  cl.ts <- factor(iris[ts.idx, 5])   # 테스트용 데이터셋의 그룹(품종) 정보
  
  pred <- knn(ds.tr, ds.ts, cl.tr, k = 5)
  acc[i] <- mean(pred==cl.ts)        # 예측 정확도
}
acc                                  # 폴드별 예측 정확도
mean(acc)                            # 폴드평균 예측 정확도
