
import pandas as pd
import matplotlib.pyplot as plt

file_name = './data/seoul-metro-2021.logs.csv'
df_raw = pd.read_csv(file_name)

file_name = './data/seoul-metro-station-info.csv'
df_station_raw = pd.read_csv(file_name)

columns = ['station.code', 'geo.latitude', 'geo.longitude']
df_station_raw = df_station_raw[columns]
df_station_raw = df_station_raw.set_index('station.code')

print('-'*50)
print(df_station_raw)

columns = ['station_code', 'people_in', 'people_out']
df_raw = df_raw[columns]

#print('-'*50)
#print(df_raw.head())

COL_STATION_CODE = 'station_code'
# station_sum = df_raw.groupby(COL_STATION_CODE).sum(numeric_only=True)
station_sum = df_raw.groupby(COL_STATION_CODE).sum()

print('-'*50)
print(station_sum)

join_data = station_sum.join(df_station_raw)

print('-'*50)
print(join_data)

join_data.to_csv('./data/seoul-metro-inout.csv')



