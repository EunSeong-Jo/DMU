score['John','Math']                # John의 수학 성적
score['Tom',c('Math','Science')]    # Tom의 수학, 과학 성적
score['Mark',]                      # Mark의 모든 과목 성적
score[,'English']                   # 모든 학생의 영어 성적
rownames(score)                     # score의 행의 이름
colnames(score)                     # score의 열의 이름
colnames(score)[2]                  # score의 열의 이름 중 두 번째 값
