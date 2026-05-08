import pandas as pd

# ── Series 생성 ──
scores = pd.Series([85, 92, 78, 95], index=["철수", "영희", "민수", "수진"])
print(scores)
# 철수    85
# 영희    92
# 민수    78
# 수진    95

# Series는 다양한 통계 메서드를 제공한다
print(scores.mean())     # 87.5  (평균)
print(scores.sum())      # 350   (합계)
print(scores.max())      # 95    (최댓값)
print(scores["영희"])    # 92    (인덱스로 접근)
print(scores[scores >= 90])  # 90점 이상만 필터링

# ── DataFrame 생성 ──
data = {
    "이름": ["철수", "영희", "민수"],
    "국어": [85, 92, 78],
    "수학": [90, 88, 95]
}
df = pd.DataFrame(data)
print(df)
#   이름  국어  수학
# 0  철수   85   90
# 1  영희   92   88
# 2  민수   78   95

# DataFrame에서 한 열을 선택하면 Series가 된다
print(type(df["국어"]))   # <class 'pandas.core.series.Series'>
print(df["국어"].mean())  # 85.0
