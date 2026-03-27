
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap

file_name = './data/seoul-metro-inout.csv'
df_raw = pd.read_csv(file_name)
df_raw = df_raw.set_index('station_code')

print('-'*50)
print(df_raw)

map = folium.Map(location=[37.50018, 126.8676],zoom_start=12)

# 히트맵 플러그인 지도에 추가하기
data_in = df_raw[['geo.latitude', 'geo.longitude','people_in']]
HeatMap(data = data_in).add_to(map)

# data_out = df_raw[['geo.latitude', 'geo.longitude','people_out']]
# HeatMap(data = data_out).add_to(map)

map.save('./map_in.html')

#map.show_in_browser()


