import pandas as pd
import numpy as np
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
data.query("date.dt.day == 15 & date.dt.month ==6", inplace=True)
'''
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
#plt.show()
'''
arima200 = sm.tsa.ARIMA(data['tmin'], order=(2, 0, 0))#fit()  # (p,d,q)
model_results = arima200.fit()
# 遍历，寻找适宜的参数
import itertools
import sys
import os
p_min = 0
d_min = 0
q_min = 0
p_max = 8
d_max = 0
q_max = 8

# Initialize a DataFrame to store the results,，以BIC准则
results_bic = pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min, p_max + 1)],
                           columns=['MA{}'.format(i) for i in range(q_min, q_max + 1)])

for p, d, q in itertools.product(range(p_min, p_max + 1),
                                 range(d_min, d_max + 1),
                                 range(q_min, q_max + 1)):
    if p == 0 and d == 0 and q == 0:
        results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = np.nan
        continue

    try:
        model = sm.tsa.ARIMA(data['tmin'], order=(p, d, q),
                             # enforce_stationarity=False,
                             # enforce_invertibility=False,
                             )
        results = model.fit()
        results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
    except:
        continue
# 热度图绘制
results_bic = results_bic[results_bic.columns].astype(float)
fig, ax = plt.subplots(figsize=(10, 8))
ax = sns.heatmap(results_bic,
                 mask=results_bic.isnull(),
                 ax=ax,
                 annot=True,
                 fmt='.2f',
                 )
ax.set_title('BIC')

train_results = sm.tsa.arma_order_select_ic(data['tmin'], ic=['aic', 'bic'], trend='nc', max_ar=4, max_ma=4)
print('AIC', train_results.aic_min_order)
print('BIC', train_results.bic_min_order)
print(sm.stats.durbin_watson(model_results.resid.values))
"""
#残差检验
resid = model_results.resid #赋值
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)

predict_sunspots = model_results.predict('2012-06', '2018-08', dynamic=True)
print(predict_sunspots)
fig, ax = plt.subplots(figsize=(12, 8))
ax = data.ix['2007':].plot(ax=ax)
predict_sunspots.plot(ax=ax)
plt.show()
"""