set.seed(101)
wordcloud(names(wordcount),     # 단어들
          freq=wordcount,       # 단어들의 빈도
          scale=c(6,0.7),       # 단어의 폰트 크기
          min.freq=3,           # 단어의 최소 빈도
          random.order=F,       # 단어의 출력 위치
          rot.per=.1,           # 90도 회전 단어 비율
          colors=pal2)          # 단어의 색
