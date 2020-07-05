import pandas as pd
import numpy as np
import datetime
import statsmodels.api as sm
from pmdarima.arima import auto_arima

'''
函数名称:datatmaxmodel
函数功能:读取清洗后的数据文件,通过分析最大值，建立ARIMA模型并进行预测,并将预测值以tmax.csv输出
输入值:无
输出值:无
'''


def datatmaxmodel(month, day):
    data_raw = pd.read_csv('thedata.csv', parse_dates=['DATE'])
    data = data_raw.loc[:, ['DATE', 'TMAX']]
    data.query("DATE.dt.year <= 2011 & DATE.dt.day == %d & DATE.dt.month == %d" % (day, month), inplace=True)
    print(data)
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
    year = dta_year[-1:].dt.year + 1
    predict_dta = pd.Series(predict_dta, index=['%d-%d-%d' % (year, month, day)], name='max')
    predict_dta.index.name = 'date'
    print(predict_dta)
    return predict_dta


'''
函数名称:datatminmodel
函数功能:读取清洗后的数据文件,通过分析最小值，建立ARIMA模型并进行预测，并将预测值以test.csv输出
输入值:无
输出值:无
'''


def datatminmodel(month, day):
    data_raw = pd.read_csv('thedata.csv', parse_dates=['DATE'])
    data = data_raw.loc[:, ['DATE', 'TMIN']]
    data.query("DATE.dt.year <= 2011 & DATE.dt.day == %d & DATE.dt.month == %d" % (day, month), inplace=True)
    print(data)
    dta_year = data['DATE']
    # 得到开始年份和结束年份
    month = dta_year[0:1].dt.month
    day = dta_year[0:1].dt.day

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
    year = dta_year[-1:].dt.year + 1
    predict_dta = pd.Series(predict_dta, index=['%d-%d-%d' % (year, month, day)], name='min')
    predict_dta.index.name = 'date'

    return predict_dta


'''
函数名称:datatavemodel
函数功能:读取清洗后的数据文件,通过分析平均值，建立ARIMA模型并进行预测,并将预测值以tave.csv输出
输入值:无
输出值:无
'''


def datatavgmodel(month, day):
    data_raw = pd.read_csv('thedata.csv', parse_dates=['DATE'])
    data = data_raw.loc[:, ['DATE', 'TAVG']]
    data.query("DATE.dt.year <= 2011 & DATE.dt.day == %d & DATE.dt.month == %d" % (day, month), inplace=True)
    print(data)
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
    year = dta_year[-1:].dt.year + 1
    predict_dta = pd.Series(predict_dta, index=['%d-%d-%d' % (year, month, day)], name='avg')
    predict_dta.index.name = 'date'
    print(predict_dta)

    return predict_dta


def data_out(predict_dta, i, data_type):
    if i == 0:
        predict_dta.to_csv('predict_result_%s.csv' % (data_type), mode='w', index=True, header=True)
    else:
        predict_dta.to_csv('predict_result_%s.csv' % (data_type), mode='a', index=True, header=False)
    with open('predict_result_%s.csv' % (data_type), 'r') as f:
        text_lines = f.readlines()
    print(text_lines)
    print()
    if text_lines[-1][3] != '9':
        tt = list(text_lines[-1])
        tt[3] = '9'
        text_lines[-1] = ''.join(tt)
        with open('predict_result_%s.csv' % (data_type), 'w') as f:
            f.writelines(text_lines)


def predict_week_data(year, month, day, data_type):
    time1 = '%d-%d-%d' % (year, month, day)
    time1 = datetime.datetime.strptime(time1, "%Y-%m-%d")
    for i in range(0, 7):
        time1 = time1 + datetime.timedelta(days=1)
        month = time1.month
        day = time1.day
        if data_type == 'min':
            predict_dta = datatminmodel(month, day)
            data_out(predict_dta, i, data_type)
        elif data_type == 'max':
            predict_dta = datatmaxmodel(month, day)
            data_out(predict_dta, i, data_type)
        elif data_type == 'avg':
            predict_dta = datatavgmodel(month, day)
            data_out(predict_dta, i, data_type)


#datatmaxmodel(7, 9)
predict_week_data(2012, 7, 9, 'min')
predict_week_data(2012, 7, 9, 'max')
predict_week_data(2012, 7, 9, 'avg')