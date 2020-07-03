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
data_raw1 = pd.read_csv(r'D:\GITHUB\Meteorological-data-analysis\thedata.csv')
data_wash = data_raw1.loc[:, ['DATE', 'TMAX']]
data_wash['DATE'] = data_wash['DATE'].apply(parser.parse)
data_wash = data_wash[(pd.Series.notnull(data_wash['TMAX']))]
data_wash.query("DATE.dt.month == 8", inplace=True)
data_wash.to_csv(r'D:\GITHUB\Meteorological-data-analysis\afterwash.csv', index=None)

data_raw2 = pd.read_csv(r'D:\GITHUB\Meteorological-data-analysis\afterwash.csv', index_col='DATE')
data = data_raw2.loc['1980':'1990', ['TMAX']]
train = data.loc['1980':'1990']
test = data.loc['1990':'1991']

print(train)

# train['diff_1'] = train['TMAX'].diff(1)
# train['diff_2'] = train['diff_1'].diff(1)
# train.plot(subplots=True, figsize=(18, 12))
#
# print(train)
# 3.1.分别画出ACF(自相关)和PACF（偏自相关）图像

# fig = plt.figure(figsize=(12, 8))
#
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(train['TMAX'], lags=20, ax=ax1)
# ax1.xaxis.set_ticks_position('bottom')
# fig.tight_layout()
#
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(train['TMAX'], lags=20, ax=ax2)
# ax2.xaxis.set_ticks_position('bottom')
# fig.tight_layout()
#plt.show()
#
# # 遍历，寻找适宜的参数
# import itertools
#
# p_min = 0
# d_min = 0
# q_min = 0
# p_max = 5
# d_max = 0
# q_max = 5
#
# # Initialize a DataFrame to store the results,，以BIC准则
# results_bic = pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min, p_max + 1)],
#                            columns=['MA{}'.format(i) for i in range(q_min, q_max + 1)])
#
# for p, d, q in itertools.product(range(p_min, p_max + 1),
#                                  range(d_min, d_max + 1),
#                                  range(q_min, q_max + 1)):
#     if p == 0 and d == 0 and q == 0:
#         results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = np.nan
#         continue
#
#     try:
#         model = sm.tsa.ARIMA(train['TMAX'], order=(p, d, q),
#                              # enforce_stationarity=False,
#                              # enforce_invertibility=False,
#                              )
#         results = model.fit()
#         results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
#     except:
#         continue
# results_bic = results_bic[results_bic.columns].astype(float)
#
# fig, ax = plt.subplots(figsize=(10, 8))
# ax = sns.heatmap(results_bic,
#                  mask=results_bic.isnull(),
#                  ax=ax,
#                  annot=True,
#                  fmt='.2f',
#                  )
# ax.set_title('BIC')
#
# # #arima200 = sm.tsa.ARIMA(data_max['TMAX'], order=(2, 0, 0)).fit()  # (p,d,q)
# # # 遍历，寻找适宜的参数
# #
# #
# # # 模型评价准则
# train_results = sm.tsa.arma_order_select_ic(train, ic=['aic', 'bic'], trend='nc', max_ar=4, max_ma=4)
#
# print('AIC', train_results.aic_min_order)
# print('BIC', train_results.bic_min_order)
# #
model = sm.tsa.ARIMA(train, order=(2, 0, 1))
results = model.fit()
predict_sunspots = results.predict(start='1985-08-01', dynamic=False)
print(predict_sunspots)
fig, ax = plt.subplots(figsize=(12, 8))
ax = train.plot(ax=ax)
predict_sunspots.plot(ax=ax)

plt.show()
