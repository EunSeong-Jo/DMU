str(iris)                 # 데이터셋 요약 정보 보기
iris[,5]                  # 품종 데이터 보기
unique(iris[,5])          # 품종의 종류 보기(중복 제거)
table(iris[,"Species"])   # 품종의 종류별 행의 개수 세기
