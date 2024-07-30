# setwd("D:/source")

######################################################
# 패키지 설치
install.packages("stringr")
library(stringr)
search()

# 패키지 이름에 ':stringr'이 들어간 패키지 검색
search()[str_detect(search(), ':stringr')]

# 메모리에 로드된 패키지의 위치 파악
searchpaths()

######################################################
if (!require(ggplot2)) {
  install.packages("ggplot2")
}
library(ggplot2)

if (!require(ggmap)) {
  install.packages("ggmap")
}
library(ggmap)

if (!require(readxl)) {
  install.packages("readxl")
}
library(readxl)

files <- c("201512","201606","201612","201706","201712")
columns <- c( "상가업소번호", "상호명", "상권업종대분류명", "상권업종중분류명",
              "상권업종소분류명", "시군구명", "행정동명", "경도", "위도")
ds.total <- NULL

getwd()

for (i in 1:length(files)) {
# filename <- paste("seoul_", files[i], ".xlsx", sep="")
  filename <- paste("Ch13\\", "seoul_", files[i], ".xlsx", sep="")
  cat("read ", filename, "...\n")               # 읽을 파일 이름 출력
  
  ds <- read_excel(filename)                    # 엑셀 파일 읽기
  ds <- data.frame(ds)                          # 데이터프레임으로 변환
  ds <- ds[,columns]                            # 분석에 필요한 변수만 추출
  ds$수집연월 <- rep(i, nrow(ds))               # 데이터 수집 시점
  ds.total <- rbind(ds.total,ds)                # 데이터 통합
}

head(ds.total)
