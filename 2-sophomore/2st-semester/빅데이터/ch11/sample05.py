
import pandas as pd
import matplotlib.pyplot as plt

from ch11.common_functon import save_csv

#### 개발자연령
file_name = './data_country.csv'
df_raw = pd.read_csv(file_name)

COLUMN_COUNTRY = 'Country'
sr_country_count = df_raw.groupby(COLUMN_COUNTRY).size()

#sr_age_count.plot.line()
#sr_age_count.plot.bar(rot = 45)
#sr_country_count.plot.barh(rot = 45)
#sr_country_count.plot.pie(figsize=(10, 10)) ##인치단위
sr_country_count.nlargest(20).plot.pie(figsize=(10, 10))

plt.tight_layout()
plt.show()