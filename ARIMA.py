import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from dateutil import parser
from scipy import stats
import statsmodels.api as sm
import statsmodels.tsa.api as smt

#数据读取与数据类型转换
data_raw = pd.read_csv(r'D:\GITHUB\Meteorological-data-analysis\thedata.csv', encoding='utf-8')
data = data_raw.loc[:, ['DATE', 'TAVG', 'TMAX', 'TMIN']]
data['DATE'] = data['DATE'].apply(parser.parse)
data['TAVG'] = data['TAVG'].astype(float)
data['TMAX'] = data['TMAX'].astype(float)
data['TMIN'] = data['TMIN'].astype(float)

#数据清洗，并将清洗后的日期和最大值存入data_max
data = data[(pd.Series.notnull(data['TMAX'])) & (pd.Series.notnull(data['TMIN']))]
data = data[(data['DATE'] >= datetime(1980, 1, 1)) & (data['DATE'] <= datetime(2016, 1, 1))]
data.query("DATE.dt.day == 15 & DATE.dt.month == 6", inplace=True)
data_max = data.loc[:, ['DATE', 'TMAX']]


print(data)

# data_max['diff_1'] = data_max['TMAX'].diff(1)
# data_max['diff_2'] = data_max['diff_1'].diff(1)
# data_max.plot(x="DATE", subplots=True, figsize=(18, 12))
#
# data_max = data_max.diff(1)
# diff1 = data_max.diff(1)
# diff2 = data_max.diff(2)

# 3.1.分别画出ACF(自相关)和PACF（偏自相关）图像

fig = plt.figure(figsize=(12, 8))

ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(data_max['TMAX'], lags=20, ax=ax1)
ax1.xaxis.set_ticks_position('bottom')
fig.tight_layout()

ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(data_max['TMAX'], lags=20, ax=ax2)
ax2.xaxis.set_ticks_position('bottom')
fig.tight_layout()


# 3.2.可视化结果

def tsplot(y, lags=None, title='', figsize=(14, 8)):
    fig = plt.figure(figsize=figsize)
    layout = (2, 2)
    ts_ax = plt.subplot2grid(layout, (0, 0))
    hist_ax = plt.subplot2grid(layout, (0, 1))
    acf_ax = plt.subplot2grid(layout, (1, 0))
    pacf_ax = plt.subplot2grid(layout, (1, 1))

    y.plot(ax=ts_ax)
    ts_ax.set_title(title)
    y.plot(ax=hist_ax, kind='hist', bins=25)
    hist_ax.set_title('Histogram')
    smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
    smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
    [ax.set_xlim(0) for ax in [acf_ax, pacf_ax]]
    sns.despine()
    plt.tight_layout()
    return ts_ax, acf_ax, pacf_ax


tsplot(data_max['TMAX'], title='Consumer Sentiment', lags=36)
plt.show()

