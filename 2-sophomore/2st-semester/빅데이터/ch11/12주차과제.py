import pandas as pd
import matplotlib.pyplot as plt

file_name = './survey_raw.csv'
df_raw = pd.read_csv(file_name)

COLUMN_COUNTRY = 'Country'
sr_country = df_raw[COLUMN_COUNTRY]

ds_data = df_raw.groupby(['Country']).size()


plt.rc('font', family='NanumBarunGothic') 

# 상위 20개 국가 데이터를 별도 저장
ds_top20 = ds_data.nlargest(20)

# 한글 매핑
country_map = {
    'United States of America': '미국',
    'India': '인도',
    'Germany': '독일',
    'United Kingdom of Great Britain and Northern Ireland': '영국',
    'Canada': '캐나다',
    'France': '프랑스',
    'Brazil': '브라질',
    'Poland': '폴란드',
    'Netherlands': '네덜란드',
    'Australia': '호주',
    'Spain': '스페인',
    'Italy': '이탈리아',
    'Russian Federation': '러시아',
    'Sweden': '스웨덴',
    'Turkey': '터키',
    'Switzerland': '스위스',
    'Austria': '오스트리아',
    'Israel': '이스라엘',
    'Iran, Islamic Republic of...': '이란',
    'Pakistan': '파키스탄'
}

# 3. .rename()을 사용해 한글로 변환
ds_top20 = ds_top20.rename(index=country_map)

# ds_data.nlargest(20).plot.pie(figsize=(10,10)) #인치단위
ds_top20.nlargest(20).plot.pie(figsize=(10,10))

plt.tight_layout()
plt.show()