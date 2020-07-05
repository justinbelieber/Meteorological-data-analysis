import pandas as pd
import numpy
import matplotlib.pyplot as pyplot
import seaborn as sns
import xgboost as xgb
from pandas import read_csv
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import load_iris

from statsmodels.tsa.arima_model import ARIMA

data_raw = pd.read_csv(r'D:\GITHUB\Meteorological-data-analysis\thedata.csv', index_col='DATE', parse_dates=['DATE'])
data = data_raw.loc['1981':'1990']['TMAX']
print(data)
data.plot()
pyplot.show()

split_point = len(data) - 7
dataset, validation = data[0:split_point], data[split_point:]
print('Dataset %d, Validation %d' % (len(dataset), len(validation)))
dataset.to_csv('dataset.csv', index=False)
validation.to_csv('validation.csv', index=False)


def difference(dataset, interval=1):
    diff = list()
    for i in range(interval+1, len(dataset)):
        value = float(dataset[i]) - float(dataset[i - interval])
        diff.append(value)
    return numpy.array(diff)


def inverse_difference(history, yhat, interval=1):
    #interval = interval+1
    return yhat + float(history[-interval])


series = read_csv('dataset.csv', header=None, index_col=None)
X = series.values
days_in_year = 365
differenced = difference(X, 365)
model = ARIMA(differenced, order=(0, 0, 1))
model_fit = model.fit(disp=0)
#print(model_fit.summary())

forecast = model_fit.forecast(steps=7)[0]
# invert the differenced forecast to something usable
history = [x for x in X]
day = 1
for yhat in forecast:
    inverted = inverse_difference(history, yhat, days_in_year)
    print('Day %d: %f' % (day, inverted))
    history.append(inverted)
    day += 1
