import yfinance as yf

stocks=["2330.TW","2345.TW","","6385.TW","2317.TW","2454.TW"]
datas = yf.download(stocks,period="10d")
datas_index = datas.reset_index()
print(datas)