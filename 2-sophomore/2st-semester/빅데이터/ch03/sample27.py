
'''
    다음 소스 코드는 40명의 학생에게 50~100점 사이의 점수를 무작위로 할당한 딕셔너리 scores를 제공한다.
    각 문제의 정답을 제시하기 위한 소스 코드를 작성하고 결과를 입력하시오.
'''
import random
import numpy as np


# Key: S10 ~ S49, S11 ~ S50

scores = dict()
for i in range(11, 50 + 1):
    scores['S' + str(i)] = random.randrange(50, 100 + 1)
print(scores)

# 40명 학생의 평균 점수를 구하시오
'''
sum = 0
for value in scores.values():
    sum += value
print(sum)
'''

# 평균
avg = sum(scores.values()) / len(scores)
print(avg)

print('-'* 30)

score_value = np.array(list(scores.values()))
avg = np.mean(score_value)
print(avg)


# 40명 중 최고 득점을 한 학생과 점수를 출력하시오.
# 여러 명인 경우, 학번이 가장 빠른 한 명만 출력되도록 하시오.




