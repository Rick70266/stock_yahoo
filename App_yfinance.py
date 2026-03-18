import yfinance as yf


def stock_info(id):
    tick = yf.Ticker(id)
    info = tick.info
    print(f'公司名稱 {info.get("shortName")}')
    print(f'最新訊息 {info.get("message")}')
    print(f'今日市場均價 {info.get("regularMarketPrice")}')
    print(f'今年度EPS {info.get("priceEPSCurrentYear")}')
    print(f'今日行情 {info.get("regularMarketRange")}')

#今日行情指數
def ticker_summary(id):
    tick = yf.Ticker(id)
    info = tick.fast_info
    #print( info )   # 今日最高最低 開盤/收盤 目前行情
    print("fast_info 通常會與即時狀況有時間差")
    print(f'開盤 {info.open}')
    print(f'今日最高{info.day_high}')
    print(f'今日最低{info.day_low}')
    print(f'目前價格{info.last_price}')

def ticker_history(id):
    tick = yf.Ticker(id)
    pdata = tick.history(period="1mo")
    print(pdata)
    print(tick.actions)
    # tick.history ( start="2025-01-01", end="2026-12-31",period = "",interval)

def ticker_download():
    stocks = ["2330.TW", "2345.TW", "AAPL", "MSFT", "NVDA", "APLE", "TSLA"]
    datas = yf.download(stocks, period="1d")
    print(datas)


#抓取台積電資訊
# stock_info("2330.TW")
# stock_info("2345.TW")

# print("===============TSMC================")
# ticker_summary("2330.TW")
# print("===============智邦================")
# ticker_summary("2345.TW")
# ticker_history("2330.TW")
ticker_download()
