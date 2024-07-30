score <- c(76, 84, 69, 50, 95, 60, 82, 71, 88, 84)
score

which(score==69)      # 성적이 69인 학생은 몇 번째에 있나
which(score>=85)      # 성적이 85 이상인 학생은 몇 번째에 있나
max(score)            # 최고 점수는 몇 점인가
which.max(score)      # 최고 점수는 몇 번째에 있나
min(score)            # 최저 점수는 몇 점인가
which.min(score)      # 최저 점수는 몇 번째에 있나

score[which(score==69)]   # 성적이 69인 성적
score[which.max(score)]   # 성적이 최대인 성적

