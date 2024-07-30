iris.new <- iris
iris.new$Species <- as.integer(iris.new$Species) # 범주형 자료를 정수로 변환
iris.new$Species

head(iris)
head(iris.new)

mod.iris <- glm(Species ~ ., data = iris.new)    # 로지스틱 회귀모델 도출
summary(mod.iris)                                # 회귀모델의 상세 내용 확인
