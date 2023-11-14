import flask
from flask import Flask, request, render_template
import pickle
import os
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing


print("app is started")
# Create flask app
flask_app = Flask(__name__)

flask_app._static_folder = 'static'

@flask_app.route("/")
def home():
    return render_template("index1.html")

@flask_app.route("/predict", methods=["POST", "GET"])
def predict():
    if request.method == 'POST' or 'GET':
        # Get the uploaded CSV file
        uploaded_file = request.files['file']
        num_months = int(request.form.get('NOM'))

        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                df.isnull().sum()
                df.dropna(inplace=True)
                df.rename(columns={'Month': 'Date', df.columns[1]: 'Sales'},
                          inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                df.index = pd.DatetimeIndex(df.index.values, freq=df.index.inferred_freq)
                train_date = df.index[-1]
                dti = pd.date_range(train_date, periods=num_months, freq="M")
                pred_start_date = dti[0]
                pred_end_date = dti[-1]

                # Load the pre-trained model
                model = pickle.load(open("Sales_Forecast.pkl", "rb"))

                # Perform the forecast
                model_SARIMA = SARIMAX(df['Sales'], order=(2, 1, 4), seasonal_order=(0, 1, 0, 12))
                model_SARIMA_fit = model_SARIMA.fit(disp=0, maxiter=200, method='nm')
                sarima_prediction = model_SARIMA_fit.predict(start=pred_start_date, end=pred_end_date)
                sarima_prediction = sarima_prediction.to_frame(name='Sarima_Predicted_Sales')
                sarima_prediction.reset_index(inplace=True)
                sarima_prediction.rename(columns={'index': 'Date'}, inplace=True)

                model_damped_holt_mul = ExponentialSmoothing(df['Sales'],trend='mul',seasonal='mul',damped_trend=True)
                results_damped_holt_mul = model_damped_holt_mul.fit()
                expo_smoothing_prediction = results_damped_holt_mul.predict(start = pred_start_date, end = pred_end_date)
                expo_smoothing_prediction = expo_smoothing_prediction.to_frame(name='Expo_Smoothing_Predicted_Sales')
                expo_smoothing_prediction.reset_index(inplace=True)
                expo_smoothing_prediction.rename(columns={'index': 'Date'}, inplace=True)

                combined_predictions = pd.merge(round(sarima_prediction), round(expo_smoothing_prediction), on='Date', how='inner')
                combined_predictions = combined_predictions.reset_index(drop=True)
                print(combined_predictions)
                return render_template('index1.html', tables=[combined_predictions.to_html(classes='data1', index=False)], titles='Predicted Sales')

            except Exception as e:
                return render_template("index1.html", prediction_text=f"Error: {str(e)}")

        else:
            return render_template("index1.html", prediction_text="Please upload a CSV file.")

if __name__ == '__main__':
    flask_app.run(debug=True)
