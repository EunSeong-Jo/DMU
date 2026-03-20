
import pandas as pd
import matplotlib.pyplot as plt

from ch11.common_functon import save_csv

file_name = '../ch11/survey_raw.csv'
df_raw = pd.read_csv(file_name)

#print('-'*50)
#print(df_raw.info())

COL_LANG = 'LanguageHaveWorkedWith'
data_lang = df_raw[COL_LANG]

#print('-'*50)
#print(data_lang)

data_lang = data_lang.str.split(';')

print('-'*50)
print(data_lang)

data_lang2 = data_lang.explode()

print('-'*50)
print(data_lang2)

data_lang3 = data_lang2.groupby(data_lang2).size()

print('-'*50)
print(data_lang3)

data_lang3.nlargest(20).plot.pie(figsize=(10, 10), autopct='%1.2f%%')
plt.tight_layout()
#plt.show()
plt.savefig('./lang_data.png')








