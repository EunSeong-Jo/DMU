# setwd("d:/source")    # myfunc.R이 저장된 폴더
# 작업 폴더: 프로젝트 폴더 
source("Ch04/myfunc.R")    # myfunc.R 안에 있는 함수 실행

# 함수 사용
a <- mydiv(20,4)      # 함수 호출
b <- mydiv(30,4)      # 함수 호출
a+b
mydiv(mydiv(20,2),5)  # 함수 호출
