b <- coef(model)[1]
W <- coef(model)[2]

speed <- 30            # 주행속도
dist <- W*speed + b
dist                   # 제동거리

speed <- 35            # 주행속도
dist <- W*speed + b
dist                   # 제동거리

speed <- 40            # 주행속도
dist <- W*speed + b
dist                   # 제동거리
