boxplot.stats(dist)

boxplot.stats(dist)$stats
# $stats
# c이 값은 박스 플롯의 주요 통계치를 나타내며, 
# 다섯 개의 숫자 요약 (Five Number Summary)이라고 불립니다. 
# 각각의 값은 다음을 의미합니다:
#   
# 정상범위 내에서의 최소값 (Minimum): 2
# 1사분위수 (Q1, 25th Percentile): 26
# 중앙값 (Median, 50th Percentile): 36
# 3사분위수 (Q3, 75th Percentile): 56
# 정상범위 내에서의 최대값 (Maximum): 93

boxplot.stats(dist)$conf
# $conf
# 이 값은 중앙값의 신뢰 구간(Confidence Interval)을 나타냅니다.
# 신뢰 구간은 중앙값의 추정치가 어느 범위에 위치할 것인지 나타내며, 
# 보통 95% 신뢰 구간을 계산합니다.
# 
# 하한 (Lower Bound): 29.29663
# 상한 (Upper Bound): 42.70337
# 이 값들은 중앙값이 해당 범위 내에 있을 것이라는 것을 나타냅니다.
