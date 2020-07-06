import pandas as pd
from fbprophet import Prophet
from dateutil import parser
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

data_raw = pd.read_csv('2199268.csv', parse_dates=['DATE'])
#data_raw.query("DATE.dt.year <= 2012 & DATE.dt.day == 5 & DATE.dt.month == 7", inplace=True)
data_raw['ds'] = data_raw['DATE']
data_raw['y'] = data_raw['TMAX'].astype(float)
df = data_raw.loc[:, ['ds', 'y']]
print(df)
df.head()
m = Prophet(changepoint_prior_scale=0.05, daily_seasonality=True,  weekly_seasonality=True)
# m = Prophet(changepoint_prior_scale=0.05)
m.fit(df)
# 构建待预测日期数据框，periods = 365 代表除历史数据的日期外再往后推 365 天
future = m.make_future_dataframe(periods=365)
future.tail()
# 预测数据集
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
# 展示预测结果
result = forecast.loc[:, ['ds', 'yhat']]
print(result)
#print(mean_squared_error(df, forecast))
m.plot(forecast)
'''
from fbprophet.diagnostics import cross_validation
df_cv = cross_validation(m, initial='730 days', period='180 days', horizon = '365 days')
df_cv.head()
from fbprophet.diagnostics import performance_metrics
df_p = performance_metrics(df_cv)
df_p.head()
from fbprophet.plot import plot_cross_validation_metric
fig = plot_cross_validation_metric(df_cv, metric='mape')
'''
result.to_csv('result.csv',  index=True, header=True)
m.plot_components(forecast)
plt.show()
