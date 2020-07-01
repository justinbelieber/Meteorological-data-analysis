
import pandas as pd
from datetime import datetime
from dateutil import parser

data_raw = pd.read_csv(r'D:\GITHUB\Meteorological-data-analysis\thedata.csv', encoding='utf-8')

data = data_raw.loc[:, ['DATE', 'TMAX', 'TMIN']]


data = data[(pd.Series.notnull(data['TMAX'])) & (pd.Series.notnull(data['TMIN']))]
#data.query("date.dt.day == 28 & date.dt.month == 6", inplace=True)
data.to_csv(r'D:\GITHUB\Meteorological-data-analysis\afterdata.csv', index=None)
