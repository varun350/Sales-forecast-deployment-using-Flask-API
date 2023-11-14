import pickle
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing


df = pd.read_csv("perrin-freres-monthly-champagne.csv")

df.isnull().sum()

df.dropna(inplace = True)

df.rename(columns={'Month': 'Date', 'Perrin Freres monthly champagne sales millions ?64-?72': 'Sales'}, inplace=True)

df['Date'] = pd.to_datetime(df['Date'])

df.set_index('Date', inplace=True)

df.index = pd.DatetimeIndex(df.index.values, freq=df.index.inferred_freq)

model_SARIMA = SARIMAX(df['Sales'], order=(2, 1, 4), seasonal_order=(0, 1, 0, 12))

model_SARIMA_fit = model_SARIMA.fit(disp=0, maxiter=200, method='nm')

model_damped_holt_mul = ExponentialSmoothing(df['Sales'],trend='mul',seasonal='mul',damped_trend=True)
results_damped_holt_mul = model_damped_holt_mul.fit()


train_date = df.index[-1]
print(train_date)
dti = pd.date_range(train_date, periods=6, freq="M")
print(dti)
pred_start_date = dti[0]
pred_end_date = dti[-1]
print(pred_start_date)
print(pred_end_date)


def pred_forecast(pred_start_date, pred_end_date):
    print("start as string")
    pred_sarima = model_SARIMA_fit.predict(start=pred_start_date, end=pred_end_date)
    pred_expo_mul = results_damped_holt_mul.predict(start = pred_start_date, end = pred_end_date)
    print(pred_sarima)
    print("end")
    return pred_sarima
#print(type(pred_SARIMA))
#pred_SARIMA = pred_SARIMA.to_frame()
#print(type(pred_SARIMA))


pickle.dump(model_SARIMA, open("Sales_Forecast.pkl", "wb"))
model = pickle.load(open('Sales_Forecast.pkl', 'rb'))

