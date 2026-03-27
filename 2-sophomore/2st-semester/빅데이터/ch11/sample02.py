
import pandas as pd
import matplotlib.pyplot as plt

from ch11.common_functon import save_csv

file_name = './survey_raw.csv'
df_raw = pd.read_csv(file_name)

COLUMN_AGE = 'Age'

print('-'*50)
print(df_raw.head())

print('-'*50)
print(df_raw[COLUMN_AGE])

sr_age = df_raw[COLUMN_AGE]

print('-'*50)
print(sr_age.unique())

print('-'*50)
print(sr_age.drop_duplicates())

print('-'*50)
print(df_raw.groupby(COLUMN_AGE).size())
print(type(df_raw.groupby(COLUMN_AGE).size()))

sr_age_count = df_raw.groupby(COLUMN_AGE).size()

index_cols = [
    'Under 18 years old'
    , '18-24 years old'
    , '25-34 years old'
    , '35-44 years old'
    , '45-54 years old'
    , '55-64 years old'
    , '65 years or older'
    , 'Prefer not to say'
]

sr_age_count = sr_age_count.reindex(index_cols)

#sr_age_count.plot.line()
#sr_age_count.plot.bar(rot = 45)
sr_age_count.plot.barh(rot = 45)

plt.tight_layout()
plt.show()












