import pandas as pd
import numpy as np
import datetime
from pmdarima.arima import auto_arima


def datatmaxmodel(year, month, day):
    data_raw = pd.read_csv('thedata.csv', parse_dates=['DATE'])
    data = data_raw.loc[:, ['DATE', 'TMAX']]
    data = data[(pd.Series.notnull(data['TMAX']))]
    data.query("DATE.dt.year <= 2020 & DATE.dt.day == %d & DATE.dt.month == %d" % (day, month), inplace=True)
    #print(data)
    dta_year = data['DATE']

    dta = data['TMAX']
    # 设置数据类型
    dta = np.array(dta, dtype=np.float)
    # 转换为Series类型的一维数组
    dta = pd.Series(dta)
    dta.index = dta_year
    dta.plot(figsize=(10, 6))

    # 使用自动模型auto_ARIMA
    arma_mod76 = auto_arima(dta, trace=True, error_action='ignore', suppress_warnings=True)
    arma_mod76.fit(dta)

    predict_dta = arma_mod76.predict(n_periods=1, exogenous=None, return_conf_int=False, alpha=0.05)
    predict_dta = pd.Series(predict_dta, index=['%d-%d-%d' % (year, month, day-1)], name='max')
    predict_dta.index.name = 'date'
    #print(predict_dta)
    return predict_dta



def datatminmodel(year, month, day):
    data_raw = pd.read_csv('thedata.csv', parse_dates=['DATE'])
    data = data_raw.loc[:, ['DATE', 'TMIN']]
    data = data[(pd.Series.notnull(data['TMIN']))]
    data.query("DATE.dt.year <= 2020 & DATE.dt.day == %d & DATE.dt.month == %d" % (day, month), inplace=True)
    #print(data)
    dta_year = data['DATE']

    dta = data['TMIN']
    # 设置数据类型
    dta = np.array(dta, dtype=np.float)
    # 转换为Series类型的一维数组
    dta = pd.Series(dta)

    dta.index = dta_year
    dta.plot(figsize=(10, 6))

    # 使用自动模型auto_ARIMA
    arma_mod76 = auto_arima(dta, trace=True, error_action='ignore', suppress_warnings=True)
    arma_mod76.fit(dta)


    # 未来一天的预测数据
    predict_dta = arma_mod76.predict(n_periods=1, exogenous=None, return_conf_int=False, alpha=0.05)
    predict_dta = pd.Series(predict_dta, index=['%d-%d-%d' % (year, month, day-1)], name='min')
    predict_dta.index.name = 'date'

    return predict_dta




def datatavgmodel(year, month, day):
    data_raw = pd.read_csv('thedata.csv', parse_dates=['DATE'])
    data = data_raw.loc[:, ['DATE', 'TAVG']]
    data = data[(pd.Series.notnull(data['TAVG']))]
    data.query("DATE.dt.year <= 2020 & DATE.dt.day == %d & DATE.dt.month == %d" % (day, month), inplace=True)
    #print(data)
    dta_year = data['DATE']

    dta = data['TAVG']
    # 设置数据类型
    dta = np.array(dta, dtype=np.float)
    # 转换为Series类型的一维数组
    dta = pd.Series(dta)
    dta.index = dta_year
    dta.plot(figsize=(10, 6))

    # 使用自动模型auto_ARIMA
    arma_mod76 = auto_arima(dta, trace=True, error_action='ignore', suppress_warnings=True)
    arma_mod76.fit(dta)

    predict_dta = arma_mod76.predict(n_periods=1, exogenous=None, return_conf_int=False, alpha=0.05)
    predict_dta = pd.Series(predict_dta, index=['%d-%d-%d' % (year, month, day-1)], name='avg')
    predict_dta.index.name = 'date'
    #print(predict_dta)

    return predict_dta


def data_out(predict_dta, i, data_type):
    if i == 0:
        predict_dta.to_csv('predict_result_%s.csv' % (data_type), mode='w', index=True, header=True)
    else:
        predict_dta.to_csv('predict_result_%s.csv' % (data_type), mode='a', index=True, header=False)
    with open('predict_result_%s.csv' % (data_type), 'r') as f:
        text_lines = f.readlines()
    #print(text_lines)
    #print()


def predict_week_data(year, month, day, data_type):
    time1 = '%d-%d-%d' % (year, month, day)
    time1 = datetime.datetime.strptime(time1, "%Y-%m-%d")
    for i in range(0, 7):
        time1 = time1 + datetime.timedelta(days=1)
        month = time1.month
        day = time1.day
        if data_type == 'min':
            predict_dta = datatminmodel(year, month, day)
            data_out(predict_dta, i, data_type)
        elif data_type == 'max':
            predict_dta = datatmaxmodel(year, month, day)
            data_out(predict_dta, i, data_type)
        elif data_type == 'avg':
            predict_dta = datatavgmodel(year, month, day)
            data_out(predict_dta, i, data_type)


predict_week_data(2020, 7, 5, 'min')
predict_week_data(2020, 7, 5, 'max')
predict_week_data(2020, 7, 5, 'avg')
