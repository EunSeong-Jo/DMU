
import pandas as pd
import matplotlib.pyplot as plt

from ch11.common_functon import save_csv

file_name = './survey_raw.csv'
df_raw = pd.read_csv(file_name)

COLUMN_AGE = 'Age'
sr_age = df_raw[COLUMN_AGE]
save_csv(sr_age, 'data_age.csv')

COLUMN_COUNTRY = 'Country'
sr_country = df_raw[COLUMN_COUNTRY]
save_csv(sr_country, 'data_country.csv')








