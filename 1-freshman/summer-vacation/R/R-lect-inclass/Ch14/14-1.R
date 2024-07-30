library(ggplot2)
setwd('D:/source')

#################################################################
## 데이터셋 준비
#################################################################
ds.2019 <- read.csv('NHIS_INCHON_2019.csv')
treat.code <- read.csv('서식코드.csv')
age.code <- read.csv('연령대코드.csv')
disease.code <- read.csv('주상병코드.csv')
dept.code <- read.csv('진료과목코드.csv')

dim(ds.2019)
View(head(ds.2019))

#################################################################
## 데이터 탐색
#################################################################

# 수진자수 
temp <- unique(ds.2019[,2:4])
nrow(temp)

# 수진자 1명당 평균 진료횟수
nrow(ds.2019)/nrow(temp)

# 수진자 남녀 비율
table(temp$성별코드)

# 수진자 연령대
age <- aggregate(temp[,'연령대코드'], by=list(연령대코드=temp$연령대코드), length)
age
age.new <- merge(age, age.code, by.x='연령대코드', by.y='코드')
names(age.new)[2] <- '수진자수' 
head(age.new)

ggplot(age.new, aes(x=reorder(연령대, 연령대코드), y=수진자수)) +
  geom_bar(stat='identity', width=0.7, fill='steelblue') +
  ggtitle('수진자 연령대 분포') +
  labs(x = '연령대') +
  coord_flip()

# 진료과별 진료횟수 비교 (상위 10개)
dept <- aggregate(ds.2019[,'진료과목코드'], by=list(진료과목코드=ds.2019$진료과목코드), length)
dept.new <- merge(dept, dept.code, by.x='진료과목코드', by.y='코드')
names(dept.new)[2] <- '진료횟수' 
dept.new <- dept.new[order(-dept.new$진료횟수),]
head(dept.new)

ggplot(dept.new[1:10, ], aes(x=reorder(진료과, 진료횟수), y=진료횟수)) +
  geom_bar(stat='identity', width=0.7, fill='steelblue') +
  ggtitle('진료과별 진료횟수') +
  labs(x = '진료과') +
  coord_flip()

# 질병별 진료횟수 비교 (상위 10개)
disease <- aggregate(ds.2019[,'주상병코드'], by=list(주상병코드=ds.2019$주상병코드), length)
disease.new <- merge(disease, disease.code, by.x='주상병코드', by.y='코드')
names(disease.new)[2] <- '진료횟수' 
disease.new <- disease.new[order(-disease.new$진료횟수),]
head(disease.new)

ggplot(disease.new[1:10, ], aes(x=reorder(질병명, 진료횟수), y=진료횟수)) +
  geom_bar(stat='identity', width=0.7, fill='steelblue') +
  ggtitle('질병별 진료횟수') +
  labs(x = '질병명') +
  coord_flip()

# 진료비가 높은 상위 10개 질병
cost <- aggregate(ds.2019[,'심결요양급여비용총액'], by=list(주상병코드=ds.2019$주상병코드), mean)
cost.new <- merge(cost, disease.code, by.x='주상병코드', by.y='코드')
names(cost.new)[2] <- '진료비' 
cost.new <- cost.new[order(-cost.new$진료비),]
cost.new$진료비 <- cost.new$진료비/10000
head(cost.new)

ggplot(cost.new[1:10, ], aes(x=reorder(질병명, 진료비), y=진료비)) +
  geom_bar(stat='identity', width=0.7, fill='steelblue') +
  ggtitle('진료비 상위 질병') +
  labs(x = '질병명', y='진료비 (단위:만원)') +
  coord_flip()

# 기관지염(J209)의 월별 진료 빈도
temp <- ds.2019[ds.2019$주상병코드=='J209', '요양개시일자']
temp <- substr(temp,5,6)
temp.freq <- data.frame(table(temp))
names(temp.freq) <- c('월','진료빈도')
temp.freq

ggplot(temp.freq, aes(x=월,y=진료빈도)) +
  geom_bar(stat='identity', width=0.7, fill='steelblue') +
  ggtitle('기관지염 월별 진료빈도') +
  labs(x = '월', y='진료비 (단위:만원)') +
  coord_flip()

# 진료형태별 진료빈도
treat <- aggregate(ds.2019[,'서식코드'], by=list(서식코드=ds.2019$서식코드), length)
treat.new <- merge(treat, treat.code, by.x='서식코드', by.y='코드')
names(treat.new)[2] <- '진료횟수' 
treat.new$진료횟수 <- treat.new$진료횟수/1000
treat.new

ggplot(treat.new, aes(x="", y=진료횟수, fill=진료형태)) +
  geom_bar(stat="identity", width=1) +
  coord_polar("y", start=0)+
  ggtitle('진료형태별 진료횟수')

