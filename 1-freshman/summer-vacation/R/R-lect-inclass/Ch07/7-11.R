sp <- split(iris, iris$Species)   # 품종별로 데이터 분리
sp                                # 분리 결과 확인
summary(sp)                       # 분리 결과 요약

sp$setosa                         # setosa 품종의 데이터 확인
sp$virginica                      # virginica 품종의 데이터 확인
