
import pandas as pd
import matplotlib.pyplot as plt

from ch11.common_functon import save_csv

file_name = '../ch11/survey_raw.csv'
df_raw = pd.read_csv(file_name)

print('-'*50)
print(df_raw.info())

COL_LANG = 'LanguageHaveWorkedWith'

data_lang = df_raw[COL_LANG]

print('data_lang: type:', type(data_lang))

print('-'*50)
print(data_lang.head())

lang_list = []

print('-'*50)
for col in data_lang:
    print(type(col))
    print(col)

    if type(col) != str:
        continue

    data_split = col.split(';')
    print(type(data_split))
    print(data_split)

    for co2 in data_split:
        print(co2)
        lang_list.append(co2)

print('-'*50)
print(lang_list)










