# install.packages("wordcloud","KoNLP","RColorBrewer")

library(wordcloud)                              # 워드클라우드
library(KoNLP)                                  # 한국어 처리
library(RColorBrewer)                           # 색상 선택 

setwd("D:/source")
text <- readLines("mis_document.txt", encoding ="UTF-8")   # 파일 읽기
buildDictionary(ext_dic = "woorimalsam")        # '우리말씀' 한글사전 로딩 
pal2 <- brewer.pal(8, "Dark2")                  # 팔레트 생성 
noun <- sapply(text,extractNoun, USE.NAMES=F)   # 명사 추출
noun                                            # 추출된 명사 출력
