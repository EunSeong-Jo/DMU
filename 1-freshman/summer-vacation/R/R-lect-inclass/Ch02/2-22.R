bt <- c('A', 'B', 'B', 'O', 'AB', 'A')  # 문자형 벡터 bt 정의
bt.new <- factor(bt)                    # 팩터 bt.new 정의
bt                                      # 벡터 bt의 내용 출력
bt.new                                  # 팩터 bt.new의 내용 출력
bt[5]                                   # 벡터 bt의 5번째 값 출력
bt.new[5]                               # 팩터 bt.new의 5번째 값 출력
levels(bt.new)                          # 팩터에 저장된 값의 종류를 출력
as.integer(bt.new)                      # 팩터의 문자값을 숫자로 바꾸어 출력
bt.new[7] <- 'B'                        # 팩터 bt.new의 7번째에 'B' 저장
bt.new[8] <- 'C'                        # 팩터 bt.new의 8번째에 'C' 저장
bt.new                                  # 팩터 bt.new의 내용 출력
