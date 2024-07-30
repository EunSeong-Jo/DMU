combn(1:5,3)                      # 1~5에서 3개를 뽑는 조합

x = c("red","green","blue","black","white")
com <- combn(x, 2)                 # x의 원소를 2개씩 뽑는 조합
com
ncol(com) # 10

for(i in 1:ncol(com)) {           # 조합을 출력
  cat(com[,i], "\n")
}
