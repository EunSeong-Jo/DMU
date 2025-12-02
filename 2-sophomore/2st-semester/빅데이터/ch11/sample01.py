import pandas as pd

from ch11.common_functon import save_csv

file_name = './survey_results_public.csv'
df_raw = pd.read_csv(file_name)

print('-'*50)
print(df_raw.head())

print('-'*50)
print(df_raw.info())

columns = ['Age', 'Country', 'LanguageHaveWorkedWith', 'LearnCode']
df_raw = df_raw[columns]

print('-'*50)
print(df_raw.info())

print('-'*50)
print(df_raw.head())

save_csv(df_raw, './survey_raw.csv')



