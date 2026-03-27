import os
import pandas as pd
from matplotlib import pyplot as plt

def get_covid_data(iso_code, rate_yn):
    file_path = './data/common_covid.csv'

    raw_df = pd.read_csv(file_path)

    # 인구비율 기준국가는 미국(USA)에 해당하는 인구수
    common_population_sr = raw_df[raw_df.iso_code == 'KOR']['population']
    common_population = common_population_sr.iat[0]

    #매개변수로 넘어온 iso_code 국가의 인구수
    cur_population_sr = raw_df[raw_df.iso_code == iso_code]['population']
    cur_population = cur_population_sr.iat[0]

    rate = round(common_population / cur_population, 2)

    filter_df = raw_df[raw_df.iso_code == iso_code]
    filter_index_df = filter_df.set_index('date')

    if rate_yn:
        return filter_index_df['total_cases'] * rate
    else:
        return filter_index_df['total_cases']
#end-def

kor_data = get_covid_data('KOR', False)
usa_data = get_covid_data('USA', False)
fra_data = get_covid_data('FRA', False)
gbr_data = get_covid_data('GBR', False)
pol_data = get_covid_data('POL', False)
index_data = kor_data.index

covid_df = pd.DataFrame({
    'KOR': kor_data,
    'USA': usa_data,
    'FRA': fra_data,
    'GBR': gbr_data,
    'POL': pol_data,
}, index = index_data)
covid_df[:].plot.line(rot = 45)



kor_data = get_covid_data('KOR', True)
usa_data = get_covid_data('USA', True)
fra_data = get_covid_data('FRA', True)
gbr_data = get_covid_data('GBR', True)
pol_data = get_covid_data('POL', True)
index_data = kor_data.index

covid_df = pd.DataFrame({
    'KOR': kor_data,
    'USA': usa_data,
    'FRA': fra_data,
    'GBR': gbr_data,
    'POL': pol_data,
}, index = index_data)
covid_df[:].plot.line(rot = 45)
plt.show()
