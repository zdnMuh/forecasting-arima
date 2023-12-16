from datetime import datetime, timedelta
import pandas as pd
from dbConf import db, dataTest, dataResult
import pmdarima as pm
import numpy as np


# Fungsi untuk memuat data dan memanggil model ARIMA serta menyimpan hasilnya ke database
def forecastArima():
    data = dataTest.query.all()
    # Load and preprocess data
    df = pd.DataFrame([(record.Date, record.Close) for record in data], columns=['Date', 'Close'])
    df.set_index('Date', inplace=True)
    series = df['Close']

    # Split data into train and test sets
    train, test = series[:-10], series[-10:]

    # Create ARIMA model
    automodel = pm.auto_arima(train, start_p=0, start_q=0, seasonal=True, trace=True, stepwise=False)

    # Make predictions
    predictionsArima = automodel.predict(n_periods=test.shape[0])

    # Save results to the database
    saveForecastResults(predictionsArima, test)

# Fungsi untuk menyimpan hasil peramalan ke tabel dataResult
def saveForecastResults(predictions_arima, test):
    for index, forecast_value in enumerate(predictions_arima):
        date_index = test.index[index]
        result = dataResult(
            Date=date_index,
            Close=test[date_index],
            Result=forecast_value
        )
        db.session.add(result)

    db.session.commit()

def calculateError():
    data = dataResult.query.all()

    if len(data) == 0:
        return "-"
    
    df = pd.DataFrame([(record.Date, record.Close, record.Result) for record in data], columns=['Date', 'Close', 'Result'])
    df.set_index('Date', inplace=True)
    data2 = df.head(7)
    series = data2['Close']
    series2 = data2['Result']
    mape = np.mean(np.abs((series2 - series) / series)) * 100
    mape = round(mape, 2)

    return mape