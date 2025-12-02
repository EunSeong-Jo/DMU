
import pandas as pd
import matplotlib.pyplot as plt

from ch11.common_functon import save_csv

#### 개발자연령
file_name = './data_age.csv'
df_raw = pd.read_csv(file_name)

COLUMN_AGE = 'Age'
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