# 메모리 제거 
rm(list = ls())

# code 5-01
favorite <- c('WINTER', 'SUMMER', 'SPRING', 'SUMMER', 'SUMMER',
              'FALL', 'FALL', 'SUMMER', 'SPRING', 'SPRING')

favorite                          # favorite의 내용 출력
table(favorite)                   # 도수분포표 계산
table(favorite)/length(favorite)  # 비율 출력

print(favorite)                          # favorite의 내용 출력
print(table(favorite))                   # 도수분포표 계산
print(table(favorite)/length(favorite))  # 비율 출력

# code 5-02
ds <- table(favorite)
ds                
barplot(ds, main='favorite season')

# code 5-03
ds <- table(favorite)
ds                
pie(ds, main='favorite season')

# code 5-04
favorite.color <- c(2, 3, 2, 1, 1, 2, 2, 1, 3, 2, 1, 3, 2, 1, 2)
ds <- table(favorite.color)
ds

barplot(ds, main='favorite color')
colors <- c('green', 'red', 'blue')
names(ds) <- colors         # 자료값 1,2,3을 green, red, blue로 변경
ds
barplot(ds, main='favorite color', col=colors)  # 색 지정 막대그래프
pie(ds, main='favorite color', col=colors)      # 색 지정 원그래프
