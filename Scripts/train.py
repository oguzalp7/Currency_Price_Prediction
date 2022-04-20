# Oguz Alp Saglam
# https://www.linkedin.com/in/oguzalp-saglam961881/

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import datetime as dt

prediction_days = 100

scaler = MinMaxScaler(feature_range=(0, 1))
dataset_dir = "../Files/pairs"
output_dir = "../Files/output"
for filename in os.listdir(dataset_dir):
    x_train = []
    y_train = []
    df = pd.read_csv(dataset_dir + "/" + filename)
    # print(df.columns)

    datetime_obj = pd.to_datetime(df.Time)
    df.Time = datetime_obj
    volume = df["Volume"] * 100.0
    df["Volume"] = volume
    df.set_index(df.Time, inplace=True)
    # print(df.head())
    
    # scale only closing price which will be the input of the LSTM Model.
    scaled_data = scaler.fit_transform(df["Close"].values.reshape(-1, 1))
    
    # train & test split.
    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x - prediction_days: x, 0])
        y_train.append(scaled_data[x, 0])
        
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # arbitrarly set hyperparameters of the model.
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)
    
    # build a communication protocol to trigger trading bot that runs on MetaTrader platform.
    file = open(output_dir + "/" + filename.split(".")[0] + ".txt", "w")
    file.write("done.")
    file.close()

    # test the model
    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime.now()
    test_data = df[start_date: end_date]
    actual_prices = test_data["Close"].values
    
    total_dataset = pd.concat((df["Close"], test_data["Close"]), axis=0)
    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.transform(model_inputs)

    # make predictions
    x_test = []

    for x in range(prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x - prediction_days: x, 0])
        
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predicted_prices = model.predict(x_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)
    # @TODO: write prediction into a file so it can be read from MT Platform. 
    # Format ==> Symbol + TimeFrame, prediction
    # as csv file.

    # visualize test results.
    plt.plot(actual_prices, color="green", label="actual prices")
    plt.plot(predicted_prices, color="orange", label="predicted prices")
    plt.legend()
    plt.show()
