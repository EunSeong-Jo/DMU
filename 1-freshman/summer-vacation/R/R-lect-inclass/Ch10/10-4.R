# 빈도수 높은데 워드클라우드에 없으면 사용자 사전에 추가
buildDictionary(ext_dic = "woorimalsam",
                user_dic=data.frame("정치", "ncn"),
                replace_usr_dic = T)
noun <- sapply(text,extractNoun, USE.NAMES=F)
noun2 <- unlist(noun)            # 추출된 명사 통합

# 무의미한 단어 제거
noun2 <- noun2[nchar(noun2)>1]   # 한 글자 단어 제거
noun2 <- gsub("하지","", noun2)  # ‘하지’ 제거
noun2 <- gsub("때문","", noun2)  # ‘때문’ 제거

wordcount <- table(noun2)        # 단어 빈도수 계산
set.seed(101)
wordcloud(names(wordcount),
          freq=wordcount,
          scale=c(6,0.7),
          min.freq=3,
          random.order=F,
          rot.per=.1,
          colors=pal2)
