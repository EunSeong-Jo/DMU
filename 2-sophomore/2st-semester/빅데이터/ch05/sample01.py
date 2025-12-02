import os
import pandas as pd

covid_file_path = '../ch04/data/owid-covid-data.csv'
raw_df = pd.read_csv(covid_file_path)

# 원하는 컬럼만
selected_columns = ['iso_code', 'location', 'date', 'total_cases', 'population']
selected_df = raw_df[selected_columns]

#South Korea
south_korea_df = selected_df[selected_df.location == 'South Korea']
print('-'*50)
print(south_korea_df.head())

#data 컬럼에 인덱스 설정
korea_date_index_df = south_korea_df.set_index('date')
print('-'*50)
print(korea_date_index_df.head())

#저장(dataframe -> csv파일로)
korea_covid_csv_file_path = './data/covid_korea.csv'
if os.path.exists(korea_covid_csv_file_path):
    os.remove(korea_covid_csv_file_path)
korea_date_index_df.to_csv('./data/covid_korea.csv', encoding='utf-8')

#locationd일 미국으로 하고, date를 인덱스로 설정하는 df
#실습!!!!

'''
#locations = df['location']
iso_code_list = raw_df['iso_code']
print('-'*50)
print(iso_code_list.unique())
'''

# USA
usa_df = selected_df[selected_df.iso_code == 'USA']
print('-'*50)
print(usa_df.head())

usa_date_index_df = usa_df.set_index('date')
print('-'*50)
print(usa_date_index_df.head())

#저장(usa dataframe -> csv파일로 저장)
usa_covid_csv_file_path = './data/covid_usa.csv'
if os.path.exists(usa_covid_csv_file_path):
    os.remove(usa_covid_csv_file_path)
usa_date_index_df.to_csv(usa_covid_csv_file_path)




















