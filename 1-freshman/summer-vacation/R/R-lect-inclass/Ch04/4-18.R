mydiv <- function(x,y=2) {
  result <- x/y
  return(result) 
}

mydiv(x=10,y=3)           # 매개변수 이름과 매개변수값을 쌍으로 입력
mydiv(10,3)               # 매개변수값만 입력
mydiv(10)                 # x에 대한 값만 입력(y 값이 생략됨)

mydiv(x <- 10,y <- 6)     # 매개변수 이름과 매개변수값을 쌍으로 입력
