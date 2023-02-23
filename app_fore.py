import flask
from flask import Flask, request, jsonify, render_template
import pickle
import os
import pandas as pd
import numpy as np

import Sales_Forecast

# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("Sales_Forecast.pkl", "rb"))


@flask_app.route("/")
def home():
    return render_template("index1.html")


@flask_app.route("/predict", methods=["POST", "GET"])
def predict():
    if request.method == "POST":
        data = request.form.get('NOM')
        print(data)
        print(type(data))
        df = pd.read_csv("perrin-freres-monthly-champagne.csv")
        df.isnull().sum()
        df.dropna(inplace=True)
        df.rename(columns={'Month': 'Date', 'Perrin Freres monthly champagne sales millions ?64-?72': 'Sales'},
                  inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.index = pd.DatetimeIndex(df.index.values, freq=df.index.inferred_freq)
        train_date = df.index[-1]
        dti = pd.date_range(train_date, periods=int(data), freq="M")
        pred_start_date1 = dti[0]
        pred_end_date1 = dti[-1]
        #int_features = [int(x) for x in request.form.values()]
        #features = [np.array(int_features)]
        #print("list", int_features)
        #print(features)
        prediction = Sales_Forecast.pred_forecast(pred_start_date1, pred_end_date1)
        prediction = prediction.to_frame(name='Sales')
        prediction.reset_index(inplace= True)
        prediction.rename(columns = {'index':'Date'}, inplace=True)
        print(prediction)


    #return render_template("index1.html", prediction_text="sales forecast for next given months is {}".format(prediction.values))
    return render_template('index1.html', tables=[prediction.to_html(classes='data1')], titles=prediction.columns.values)
    #return render_template('index1.html', prediction_text="sales forecast for next given months is {}", titles=prediction.columns.values)
    #return "success"


if __name__ == "__main__":
    flask_app.run(debug=True)

