from myXgb import *
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from xgboost.sklearn import XGBRegressor  # wrapper
import scipy.stats as st
import warnings

warnings.filterwarnings('ignore')
config_plot()

data_raw = pd.read_csv(r'D:\GITHUB\Meteorological-data-analysis\tian_jin.csv', index_col='DATE', parse_dates=['DATE'])
df = data_raw.loc['1960':'2021', ['TMAX', 'TAVG', 'TMIN']]

df.to_csv('df.csv')

print(df)
# base parameters
xgb_params = {
    'booster': 'gbtree',
    'objective': 'reg:linear',  # regression task
    'subsample': 0.80,  # 80% of data to grow trees and prevent overfitting
    'colsample_bytree': 0.85,  # 85% of features used
    'eta': 0.1,
    'max_depth': 6,
    'seed': 42}  # for reproducible results

val_ratio = 0.3
ntree = 300
early_stop = 50

print('-----Xgboost Using All Numeric Features-----',
      '\n---inital model feature importance---')


#############################################################################

G_power = df["TMAX"]


df.dropna(inplace=True)
df.iloc[-1, :].index

test_start_date = '2000-07-01'
unseen_start_date = '2020-07-01'

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
               'max_depth': st.randint(6, 30)
               }
search_sk = RandomizedSearchCV(
    skrg, params_grid, cv=5, random_state=1, n_iter=20)  # 5 fold cross validation

print(X_train, y_train)

search_sk.fit(X, Y)

# best parameters
print("best parameters:", search_sk.best_params_); print(
    "best score:", search_sk.best_score_)
# with new parameters
params_new = {**params_sk, **search_sk.best_params_}

model_final = xgb.train(params_new, dtrain, evals=watchlist,
                        early_stopping_rounds=early_stop, verbose_eval=True)

importance = model_final.get_fscore()
importance_sorted = sorted(importance.items(), key=operator.itemgetter(1))
fig1 = feature_importance_plot(importance_sorted, 'feature importance')
plt.show()

#############################################################################
Y_hat = model_final.predict(X_test)
Y_hat = pd.DataFrame(Y_hat, index=Y_test.index, columns=["predicted"])

# predictions to unseen future data
unseen_y = model_final.predict(X_unseen)

print(X_unseen)

forecasts = pd.DataFrame(
    unseen_y, index=df_unseen.index, columns=["forecasts"])

plot_start = '2015'
print('--------------------------Xgboost-----------------------------')
forecasts_plot1 = xgb_forecasts_plot(
    plot_start, Y, Y_test, Y_hat, forecasts, 'Initial Model')

forecasts.to_csv('hai_nan_forecast_max.csv')


