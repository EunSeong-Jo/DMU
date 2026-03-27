import pandas as pd
import matplotlib.pyplot as plt
from ch05.common_function import init_plt

#한글폰트설정
init_plt()

COL_POPULATION = 'population'
COL_TOTAL_CASES = 'total_cases'

# file_path에 대한 데이터 리턴 함수(dataframe)
def get_covid_data_series(file_path):
    df = pd.read_csv(file_path)
    index_df = df.set_index('date')

    #TODO: 은선아 이코드 확인좀!!!
    population = df[COL_POPULATION].iat[0]

    return {
        COL_POPULATION: population,
        'data_sr': index_df[COL_TOTAL_CASES]
    }
#end-def

kor_data = get_covid_data_series('../ch05/data/covid_korea.csv')
kor_data_index = kor_data['data_sr'].index

hi_data = get_covid_data_series('./hi_covid_data.csv')
hi_data_index = hi_data['data_sr'].index

#2개의 인덱스를 합침.
data_index = kor_data_index.union(hi_data_index)

##################################################################
#인구비율 구하기!!!!!
rate = round(kor_data[COL_POPULATION] / hi_data[COL_POPULATION], 2)

covid_df = pd.DataFrame(
    {
        '대한민국': kor_data['data_sr'],
        '하와이': hi_data['data_sr'] * rate
    }, index = data_index)
covid_df.plot.line()
plt.show()