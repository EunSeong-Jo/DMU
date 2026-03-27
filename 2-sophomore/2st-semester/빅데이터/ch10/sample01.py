import os

import pandas as pd

file_path = './hawaii-covid-data.csv'
df_raw = pd.read_csv(file_path)

print('-'*50)
print(df_raw.head())

print('-'*50)
print(df_raw.info())

df_raw['date'] = pd.to_datetime(df_raw['submission_date'])

#2021년도 하와이 인구수: 1,441,553명
df_raw['population'] = 1441553
df_raw['total_cases'] = df_raw['tot_cases']

print('-'*50)
print(df_raw.info())

hi_columns = ['date', 'total_cases', 'population']
df_raw_filter = df_raw[hi_columns]
print('-'*50)
print(df_raw_filter.head())

print('-'*50)
print(df_raw_filter.info())

df_raw_filter.set_index('date', inplace=True)

print('-'*50)
print(df_raw_filter.head())

#저장(usa dataframe -> csv파일로 저장)
hi_file_path = './hi_covid_data.csv'
if os.path.exists(hi_file_path):
    os.remove(hi_file_path)
df_raw_filter.to_csv(hi_file_path)


#print('-'*50)
#print(df_raw_filter['date'].dt.year.unique())

'''
#날짜, 감염자수, 인구수
#df_raw 데이터프레임에 population컬럼을 추가
df_raw['population'] = 0



# df_raw_filter['date'] = pd.to_datetime(df_raw_filter['submission_date'])

print('-'*50)
print(df_raw_filter.info())
'''