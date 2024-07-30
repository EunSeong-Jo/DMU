d <- c(1,2,3,4,5,6,7,8,9,10)
sum(d)                          # d에 포함된 값들의 합
sum(2*d)                        # d에 포함된 값들에 2를 곱한 후 합한 값
length(d)                       # d에 포함된 값들의 개수
mean(d[1:5])                    # 1~5번째 값들의 평균
max(d)                          # d에 포함된 값들의 최댓값
min(d)                          # d에 포함된 값들의 최솟값
sort(d)                         # 오름차순 정렬
sort(d, decreasing = FALSE)     # 오름차순 정렬
sort(d, decreasing = TRUE)      # 내림차순 정렬
v1 <- median(d)
v1
v2 <- sum(d)/length(d)
v2
