import pandas as pd
import matplotlib.pyplot as plt
from ch05.common_function import init_plt

#한글폰트설정
init_plt()

# file_path에 대한 데이터 리턴 함수(dataframe)
def get_covid_data_series(file_path):
    kor_df = pd.read_csv(file_path)
    kor_index_df = kor_df.set_index('date')
    return kor_index_df['total_cases']
#end-def

kor_data = get_covid_data_series('../ch05/data/covid_korea.csv')
usa_data = get_covid_data_series('../ch05/data/covid_usa.csv')
#index_data = kor_data.index
index_data = usa_data.index

print('kor_data type:', type(kor_data))

rate = 6.53

covid_df = pd.DataFrame(
    {
        '대한민국': kor_data * rate,
        '미국': usa_data
    }, index = index_data)
#covid_df['2022-01-01':'2022-12-31'].plot.line(rot = 45)
covid_df[:].plot.line(rot = 45)
plt.show()
