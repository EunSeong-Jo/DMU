library(ggplot2)
setwd('D:/source')

#################################################################
## 데이터셋 준비
#################################################################
ds.2019 <- read.csv('NHIS_INCHON_2019.csv')
ds.2020 <- read.csv('NHIS_INCHON_2020.csv')
treat.code <- read.csv('서식코드.csv')
age.code <- read.csv('연령대코드.csv')
disease.code <- read.csv('주상병코드.csv')
dept.code <- read.csv('진료과목코드.csv')

ds.2020$요양개시일자  <-  gsub("-", "", ds.2020$요양개시일자)
ds.tot <- rbind(ds.2019, ds.2020)
ds.tot$기준년도 <- factor(ds.tot$기준년도)
dim(ds.tot)

#################################################################
## 코로나19 이전, 이후 비교
#################################################################

# 연도별 연령대별 수진자수 비교
temp <- unique(ds.tot[,1:4])
age <- aggregate(temp[,c('기준년도','연령대코드')], 
                 by=list(기준년도=temp$기준년도,연령대코드=temp$연령대코드), 
                 length)
age <- age[,1:3]
age.new <- merge(age, age.code, by.x='연령대코드', by.y='코드')
names(age.new)[3] <- '수진자수' 
head(age.new)

ggplot(age.new, aes(x=reorder(연령대, 연령대코드), y=수진자수, 
                    colour=기준년도, group=기준년도)) +
  geom_line() +
  geom_point(size=6, shape=19, alpha=0.5) +
  ggtitle('연도별 수진자 연령대 분포') +
  labs(x = '연령대') + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

# 연도별 진료과별 진료횟수 비교 
dept <- aggregate(ds.tot[,c('기준년도','진료과목코드')], 
                  by=list(기준년도=ds.tot$기준년도,진료과목코드=ds.tot$진료과목코드), 
                  length)
dept <- dept[,1:3]
dept.new <- merge(dept, dept.code, by.x='진료과목코드', by.y='코드')
names(dept.new)[3] <- '진료횟수' 
head(dept.new)

ggplot(dept.new, aes(x=진료과, y=진료횟수, 
                     colour=기준년도, group=기준년도)) +
  geom_line() +
  geom_point(size=6, shape=19, alpha=0.5) +
  ggtitle('연도별 진료과별 진료횟수 분포') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

# 내과 질환 월별 진료건수 추이 비교 
temp <- ds.tot[ds.tot$진료과목코드==1, c('기준년도','요양개시일자')]
temp$month <- substr(temp$요양개시일자,5,6)
temp.agg <- aggregate(temp, 
                      by=list(기준년도=temp$기준년도,월=temp$month), length)
temp.agg <- temp.agg[,1:3]
names(temp.agg)[3] <- '진료횟수'
head(temp.agg)

ggplot(temp.agg, aes(x=월, y=진료횟수, 
                     colour=기준년도, group=기준년도)) +
  geom_line() +
  geom_point(size=6, shape=19, alpha=0.5) +
  ggtitle('연도별 월별 내과 진료횟수 분포') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

