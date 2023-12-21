import yfinance as yf

def ambil():
    symbol = "ANTM.JK"
    stock_data = yf.download(symbol, start="2022-01-01", end="2023-01-01")

    print(stock_data.index)