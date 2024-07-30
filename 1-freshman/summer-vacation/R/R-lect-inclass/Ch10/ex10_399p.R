library(wordcloud)                             
library(KoNLP)                                  
library(RColorBrewer)                          
setwd("D:/source")
text <- readLines("링컨_취임사.txt", encoding ="UTF-8" )   # 파일 읽기

buildDictionary(ext_dic = "woorimalsam")         # '우리말씀' 한글사전 로딩 
pal2 <- brewer.pal(8, "Dark2")                   # 팔레트 생성 
noun <- sapply(text,extractNoun, USE.NAMES=F)    # 명사 추출

noun2 <- unlist(noun)             # 추출된 명사 통합
noun2 <- noun2[nchar(noun2)>1]    # 한 글자 이하 단 제거
wordcount <- table(noun2)         # 단어 빈도수 계산
wordcount

set.seed(101)
wordcloud(names(wordcount),     # 단어들
          freq=wordcount,       # 단어들의 빈도 
          scale=c(6,0.7),       # 단어의 폰트 크기
          min.freq=2,           # 단어의 최소빈도 
          random.order=F,       # 단어의 출력 위치
          rot.per=.1,           # 90도 회전 단어 비율 
          colors=pal2)          # 단어 색
