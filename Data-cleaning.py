
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from dateutil import parser

data_raw = pd.read_csv(r'D:\GITHUB\Meteorological-data-analysis\thedata.csv', encoding='utf-8')

data = data_raw.loc[:, ['DATE', 'TAVG', 'TMAX', 'TMIN']]
data['DATE']=data['DATE'].apply(parser.parse)

data = data[(pd.Series.notnull(data['TMAX'])) & (pd.Series.notnull(data['TMIN']))]
data.query("DATE.dt.day == 15", inplace=True)
#data.to_csv(r'D:\GITHUB\Meteorological-data-analysis\afterdata.csv', index=None)

plt.figure(figsize=(20, 20))

plt.plot(data['DATE'], data['TMAX'])
plt.show()