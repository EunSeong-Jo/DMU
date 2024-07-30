weight <- c(60, 62, 64, 65, 68, 69)
weight.heavy <- c(weight, 120)
weight
weight.heavy

mean(weight)                    # 평균
mean(weight.heavy)              # 평균

median(weight)                  # 중앙값
median(weight.heavy)            # 중앙값

mean(weight, trim=0.2)          # 절사평균(상하위 20% 제외)
mean(weight.heavy,trim=0.2)     # 절사평균(상하위 20% 제외)
