import numpy
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score

from util import *
from myXgb import *
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from xgboost.sklearn import XGBRegressor  # wrapper
import scipy.stats as st
import warnings

warnings.filterwarnings('ignore')
config_plot()


##############################################################################
# we only focus on the last 18000 points for datetime information
# Run xgboost on all features
# get data
# N_rows = 18000
# parse_dates = [['Date', 'Time']]
# filename = "household_power_consumption.txt"
# encode_cols = ['Month', 'DayofWeek', 'Hour']
#
# df = preprocess(N_rows, parse_dates, filename)
# # keep all features
# df = date_transform(df, encode_cols)
# print(parse_dates)
data_raw = pd.read_csv(r'D:\GITHUB\Meteorological-data-analysis\thedata.csv', index_col='DATE', parse_dates=['DATE'])
df = data_raw.loc['1981':'2011', ['TMIN', 'TAVG', 'TMAX']]
# df = df.replace(np.nan, '?')
# df[df == '?'] = 0
# # df['TMAX' == '?'] = numpy.nan
# imputer = SimpleImputer()
# imputed_x = imputer.fit_transform(df)
df.to_csv('df.csv')
#df = [pd.Series.notnull(df['TMAX'])]
print(df)
# base parameters
xgb_params = {
    'booster': 'gbtree',
    'objective': 'reg:linear',  # regression task
    'subsample': 0.80,  # 80% of data to grow trees and prevent overfitting
    'colsample_bytree': 0.85,  # 85% of features used
    'eta': 0.1,
    'max_depth': 10,
    'seed': 42}  # for reproducible results

val_ratio = 0.3
ntree = 300
early_stop = 50

print('-----Xgboost Using All Numeric Features-----',
      '\n---inital model feature importance---')
# fig_allFeatures = xgb_importance(
#     df, val_ratio, xgb_params, ntree, early_stop, 'All Features')
# plt.show()

#############################################################################
# xgboost using only datetime information
#bucket_size = "5T"
#df = preprocess(N_rows, parse_dates, filename)
G_power = df["TMAX"]

#df = pd.DataFrame(bucket_avg(G_power, bucket_size))

df.dropna(inplace=True)
df.iloc[-1, :].index  # last time step  #2010-11-26 21:00:00

test_start_date = '2010-07-25'
unseen_start_date = '2011-01-01'
#steps = 200
# get splited data
df_unseen, df_test, df = xgb_data_split(
    df, unseen_start_date, test_start_date, ['TMAX'])
print('\n-----Xgboost on only datetime information---------\n')
print(df_unseen)
dim = {'train and validation data ': df.shape,
       'test data ': df_test.shape,
       'forecasting data ': df_unseen.shape}
print(pd.DataFrame(list(dim.items()), columns=['Data', 'dimension']))

# train model
Y = df.iloc[:, 0]
X = df.iloc[:, 1:]



X_train, X_val, y_train, y_val = train_test_split(X, Y,
                                                  test_size=val_ratio,
                                                  random_state=42)

X_test = xgb.DMatrix(df_test.iloc[:, 1:])
Y_test = df_test.iloc[:, 0]
X_unseen = xgb.DMatrix(df_unseen)

dtrain = xgb.DMatrix(X_train, y_train)
dval = xgb.DMatrix(X_val, y_val)
watchlist = [(dtrain, 'train'), (dval, 'validate')]

# Grid Search
params_sk = {
    'objective': 'reg:linear',
    'subsample': 0.8,
    'colsample_bytree': 0.85,
    'seed': 42}

skrg = XGBRegressor(**params_sk)

skrg.fit(X_train, y_train)

params_grid = {"n_estimators": st.randint(100, 500),
               #                "colsample_bytree": st.beta(10, 1),
               #                "subsample": st.beta(10, 1),
               #                "gamma": st.uniform(0, 10),
               #                'reg_alpha': st.expon(0, 50),
               #                "min_child_weight": st.expon(0, 50),
               #               "learning_rate": st.uniform(0.06, 0.12),
               'max_depth': st.randint(6, 30)
               }
search_sk = RandomizedSearchCV(
    skrg, params_grid, cv=5, random_state=1, n_iter=20)  # 5 fold cross validation

print(X,Y)

search_sk.fit(X, Y)

# best parameters
print("best parameters:", search_sk.best_params_); print(
    "best score:", search_sk.best_score_)
# with new parameters
params_new = {**params_sk, **search_sk.best_params_}

model_final = xgb.train(params_new, dtrain, evals=watchlist,
                        early_stopping_rounds=early_stop, verbose_eval=True)

print('-----Xgboost Using Datetime Features Only------',
      '\n---Grid Search model feature importance---')
importance = model_final.get_fscore()
importance_sorted = sorted(importance.items(), key=operator.itemgetter(1))
fig1 = feature_importance_plot(importance_sorted, 'feature importance')
plt.show()

#############################################################################
# Forcasting
# prediction to testing data
Y_hat = model_final.predict(X_test)
Y_hat = pd.DataFrame(Y_hat, index=Y_test.index, columns=["predicted"])

# predictions to unseen future data
unseen_y = model_final.predict(X_unseen)
forecasts = pd.DataFrame(
    unseen_y, index=df_unseen.index, columns=["forecasts"])

# plot forcast results using grid search final model
plot_start = '2006'
print('-----Xgboost Using Datetime Features Only------',
      '\n---Forecasting from Grid Search---')
forecasts_plot2 = xgb_forecasts_plot(
    plot_start, Y, Y_test, Y_hat, forecasts, 'Grid Search')

# forcasts results using itinial model
xgb_model = xgb.train(xgb_params, dtrain, ntree, evals=watchlist,
                      early_stopping_rounds=early_stop, verbose_eval=False)
Y_hat = xgb_model.predict(X_test)
Y_hat = pd.DataFrame(Y_hat, index=Y_test.index, columns=["test_predicted"])
unseen_y = xgb_model.predict(X_unseen)
forecasts = pd.DataFrame(
    unseen_y, index=df_unseen.index, columns=["forecasts"])
plot_start = '2006'
print('-----Xgboost Using Datetime Features Only------',
      '\n---Forecasting from initial---')
forecasts_plot1 = xgb_forecasts_plot(
    plot_start, Y, Y_test, Y_hat, forecasts, 'Initial Model')

forecasts.to_csv('forecast.csv')


