from dbConf import db, dataTrain, dataTest, dataResult
import yfinance as yf
from datetime import datetime

# Fungsi untuk menyimpan data ke dalam tabel dataTest
def saveScrape(symbol, startDate, endDate):
    data = yf.download(symbol, start=startDate, end=endDate)

    for index, row in data.iterrows():
        data_train = dataTrain(
            Date=index.date(),
            Open=row['Open'],
            High=row['High'],
            Low=row['Low'],
            Close=row['Close'],
            Adj=row['Adj Close'],
            Volume=row['Volume']
        )
        db.session.add(data_train)

    db.session.commit()
