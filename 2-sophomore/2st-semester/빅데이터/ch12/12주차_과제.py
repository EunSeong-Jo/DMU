import pandas as pd
import matplotlib.pyplot as plt

file_name = 'C:/Users/asus/DMU/2-sophomore/2st-semester/빅데이터/ch11/survey_raw.csv' 
df_raw = pd.read_csv(file_name)

COL_AGE = 'Age'
COL_LANG = 'LanguageHaveWorkedWith'

df_age = df_raw[df_raw[COL_AGE] == '35-44 years old']

data_lang = df_raw[COL_LANG].str.split(';') 

data_lang_exploded = data_lang.explode() 

data_lang_counts = data_lang_exploded.groupby(data_lang_exploded).size()

data_lang_counts.nlargest(5).plot.pie(figsize=(10, 10), autopct='%1.2f%%')

plt.tight_layout()
output_filename = './12주차_파이차트.png' 
plt.savefig(output_filename)
plt.show()