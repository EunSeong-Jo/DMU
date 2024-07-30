temp <- quakes # 피지(Fiji) 지역에서 발생한 지진에 대한 정보

# 열(변수) 5개
# lat: 지진의 위도 (latitude)
# long: 지진의 경도 (longitude)
# depth: 지진의 깊이 (km 단위)
# mag: 지진의 규모 (리히터 규모)
# stations: 지진을 감지한 관측소의 수
head(temp)

temp$group <- 'A'
temp$group[temp$long>=180] <- 'B'
head(temp)

boxplot(mag~group, data=temp, main="경도별 진도 분포")
