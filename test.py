import pandas as pd
from datetime import datetime
from dateutil import parser
import matplotlib.pylab as plt
import statsmodels.api as sm
import statsmodels.formula as smf
import statsmodels.tsa.api as smt
import seaborn as sns
data_raw = pd.read_csv('2199268.csv', encoding='utf-8')
data_raw['date'] = data_raw['DATE'].apply(parser.parse)
data_raw['tmax'] = data_raw['TMAX'].astype(float)
data_raw['tmin'] = data_raw['TMIN'].astype(float)
data = data_raw.loc[:, ['date', 'tmax', 'tmin']]
data = data[(pd.Series.notnull(data['tmax'])) & (pd.Series.notnull(data['tmin']))]
data = data[(data['date'] >= datetime(1980, 1, 1)) & (data['date'] <= datetime(2016, 1, 1))]
data.query("date.dt.day == 28 & date.dt.month ==6", inplace=True)
data['diff1'] = data['tmin'].diff(1)  # 一阶差分
data['diff2'] = data['diff1'].diff(1)  # 二阶差分
# data.to_csv('maxmin.csv', index=None)
data.plot(x='date', subplots=True, figsize=(18, 12))
plt.figure(figsize=(12, 8))
plt.plot(data['date'], data['tmin'])
plt.figure(figsize=(12, 8))
plt.plot(data['date'], data['diff1'])
plt.figure(figsize=(12, 8))
plt.plot(data['date'], data['diff2'])
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(data['tmin'], lags=20, ax=ax1)
ax1.xaxis.set_ticks_position('bottom')
fig.tight_layout()

ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(data['tmin'], lags=20, ax=ax2)
ax2.xaxis.set_ticks_position('bottom')
fig.tight_layout()
plt.show()