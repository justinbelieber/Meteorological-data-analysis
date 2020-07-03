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
data_raw = pd.read_csv(r'D:\GITHUB\Meteorological-data-analysis\thedata.csv', index_col='DATE', parse_dates=['DATE'])
data = data_raw.loc[:, ['TAVG', 'TMAX', 'TMIN']]
# data['DATE'] = data['DATE'].apply(parser.parse)
data['TAVG'] = data['TAVG'].astype(float)
data['TMAX'] = data['TMAX'].astype(float)
data['TMIN'] = data['TMIN'].astype(float)

#数据清洗，并将清洗后的日期和最大值存入data_max
data = data[(pd.Series.notnull(data['TMAX'])) & (pd.Series.notnull(data['TMIN']))]
data.query("DATE.dt.day == 15 & DATE.dt.month == 6", inplace=True)
data_max = data.loc[:, ['TMAX']]
# data_max['DATA'] = datetime.now().strftime('%Y-%m-%d')

print(data_max)

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

# 遍历，寻找适宜的参数
import itertools

p_min = 0
d_min = 0
q_min = 0
p_max = 5
d_max = 0
q_max = 5

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
        model = sm.tsa.ARIMA(data_max['TMAX'], order=(p, d, q),
                             # enforce_stationarity=False,
                             # enforce_invertibility=False,
                             )
        results = model.fit()
        results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
    except:
        continue
results_bic = results_bic[results_bic.columns].astype(float)

fig, ax = plt.subplots(figsize=(10, 8))
ax = sns.heatmap(results_bic,
                 mask=results_bic.isnull(),
                 ax=ax,
                 annot=True,
                 fmt='.2f',
                 )
ax.set_title('BIC')

#arima200 = sm.tsa.ARIMA(data_max['TMAX'], order=(2, 0, 0)).fit()  # (p,d,q)
# 遍历，寻找适宜的参数


# 模型评价准则
train_results = sm.tsa.arma_order_select_ic(data_max['TMAX'], ic=['aic', 'bic'], trend='nc', max_ar=4, max_ma=4)

print('AIC', train_results.aic_min_order)
print('BIC', train_results.bic_min_order)

model = sm.tsa.ARIMA(data_max['TMAX'], order=(0, 0, 1))
results = model.fit()
predict_sunspots = results.predict(dynamic=False)
print(predict_sunspots)
fig, ax = plt.subplots(figsize=(12, 8))
ax = data_max['TMAX'].plot(ax=ax)
predict_sunspots.plot(ax=ax)

plt.show()
