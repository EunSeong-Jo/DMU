install.packages("treemap")

library(treemap)    # treemap 패키지 불러오기

# 데이터셋 GNI2014
# iso3: 국가의 ISO 3166-1 알파-3 코드.
# country: 국가 이름.
# continent: 국가가 속한 대륙.
# population: 2014년의 인구 수.
# GNI: 2014년의 국민총소득 (백만 달러 단위).

data(GNI2014)                          # 데이터 불러오기
str(GNI2014)
head(GNI2014)                          # 데이터 내용보기

treemap(GNI2014,
        index=c("continent","iso3"),   # 계층구조 설정(대륙-국가)
        vSize="population",            # 타일의 크기
        vColor="GNI",                  # 타일의 컬러
        type="value",                  # 타일 컬러링 방법
        title="World's GNI")           # 트리맵 제목
