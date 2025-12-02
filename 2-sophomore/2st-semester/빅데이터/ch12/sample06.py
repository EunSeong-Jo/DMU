
import pandas as pd
import matplotlib.pyplot as plt
from folium import folium
from folium.plugins import HeatMap

file_name = './data/seoul-metro-2021.logs.csv'
df_raw = pd.read_csv(file_name)

file_name = './data/seoul-metro-station-info.csv'
df_station_raw = pd.read_csv(file_name)

columns = ['station.code', 'geo.latitude', 'geo.longitude']
df_station_raw = df_station_raw[columns]
df_station = df_station_raw.set_index('station.code')

print('-'*50)
print(df_raw)

print('-'*50)
print(df_raw.info())

df_raw['timestamp'] = pd.to_datetime(df_raw['timestamp'])

print('-'*50)
print(df_raw.info())

print('-'*50)
print(df_raw)

columns = ['station_code', 'people_in', 'people_out']
data_in = df_raw[columns][ df_raw['timestamp'].dt.hour <= 9 ].groupby('station_code').sum()

print('-'*50)
print(data_in)

join_in = data_in.join(df_station)

print('-'*50)
print(join_in)

map = folium.Map(location=[37.50018, 126.8676],zoom_start=12)

# 히트맵 플러그인 지도에 추가하기
HeatMap(data = join_in[['geo.latitude', 'geo.longitude', 'people_in']]).add_to(map)
map.show_in_browser()
