import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
from dbConf import dataTest, dataResult, db

def forecastArima():
    # Mengasumsikan 'dataTest' adalah model dan 'Date', 'Close' adalah kolom di model tersebut
    data = dataTest.query.all()

    df = pd.DataFrame([(d.Date, d.Close) for d in data], columns=['date', 'close'])
    df.set_index('date', inplace=True)

    # Membuat model ARIMA
    stepwise_fit = auto_arima(df['close'], trace=True, suppress_warnings=True)
    model = ARIMA(df['close'], order=stepwise_fit.order)
    results = model.fit()

    # Melakukan peramalan untuk beberapa langkah ke depan
    forecast_steps = 10
    forecast = results.get_forecast(steps=forecast_steps)
    forecast_values = forecast.predicted_mean

    # Menambahkan hasil peramalan ke DataFrame
    df=df.tail(10)
    df['result'] = forecast_values.values

    # Menyimpan hasil peramalan ke tabel hasil di database Flask
    for index, row in df.iterrows():
        result = dataResult(
            Date=index,
            Close=row['close'],
            Result=row['result']
        )
        db.session.add(result)

    db.session.commit()