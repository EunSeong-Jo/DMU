noun2 <- unlist(noun)                        # 추출된 명사 통합
wordcount <- table(noun2)                    # 단어 빈도수 계산
temp <- sort(wordcount, decreasing=T)[1:10]  # 빈도수 높은 단어 10개 추출
temp
temp <- temp[-1]                             # 공백 단어 제거
barplot(temp,                                # 막대그래프 작성
        names.arg = names(temp),             # 막대 이름을 단어로 표시
        col ="lightblue",                    # 막대의 색상 지정
        main ="빈도수 높은 단어", ylab = "단어 빈도수")
