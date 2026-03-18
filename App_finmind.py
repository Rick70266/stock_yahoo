

from FinMind.data import DataLoader

dl = DataLoader()


df = dl.taiwan_stock_daily(stock_id="2330", start_date="2026-03-17", end_date="2026-03-19")
print(df)