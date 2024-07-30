st <- data.frame(state.x77)        # 매트릭스를 데이터프레임으로 변환
symbols(st$Illiteracy, st$Murder,  # 원의 x, y 좌표의 열
        circles=st$Population,     # 원의 반지름의 열
        inches=0.3,                # 원의 크기 조절값
        fg="skyblue",              # 원의 테두리 색
        bg="lightgray",            # 원의 바탕색
        lwd=1.5,                   # 원의 테두리선 두께
        xlab="rate of Illiteracy",
        ylab="crime(murder) rate",
        main="Illiteracy and Crime")

text(st$Illiteracy, st$Murder,     # 텍스트가 출력될 x, y 좌표
     rownames(st),                 # 출력할 텍스트
     cex=0.6,                      # 폰트 크기
     col="brown")                  # 폰트 컬러

# 살인률 최고 10개
st[order(st$Murder, decreasing = T), ][1:10, ]
# 문맹률 최고 10개
st[order(st$Illiteracy, decreasing = T), ][1:10, ]
