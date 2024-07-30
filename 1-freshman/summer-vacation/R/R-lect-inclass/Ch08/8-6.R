ggplot(df, aes(x=month,y=rain)) +         # 그래프를 그릴 데이터 지정
  geom_bar(stat="identity",               # 막대 높이는 y축에 해당하는 열의 값
           width=0.7,                     # 막대의 폭 지정
           fill="steelblue") +            # 막대의 색 지정
  ggtitle("월별 강수량") +                # 그래프의 제목 지정
  theme(plot.title = element_text(size=25, face="bold", colour="steelblue")) +
  labs(x="월",y="강수량") +               # 그래프의 x, y축 레이블 지정
  coord_flip()                            # 그래프를 가로 방향으로 출력
