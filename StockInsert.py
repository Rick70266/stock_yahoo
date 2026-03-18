import yfinance as yf
import pymssql
import time
from datetime import datetime

# --- 設定區 ---
DB_CONFIG = {
    "server": "rickisme0022.database.windows.net",
    "user": "rickisme0022",
    "password": "r0932621147R",  # <--- 請改回你的正確密碼
    "database": "free-sql-db-5276415"
}

# 建立代號與名稱的對照表，避免 yfinance 抓不到名稱導致 SQL 報錯
STOCK_MAP = {
    "2330.TW": "台積電",
    "2345.TW": "智邦"
}

def fetch_and_save():
    conn = None
    try:
        # 建立資料庫連線
        conn = pymssql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        now = datetime.now()
        current_time_str = now.strftime("%H:%M:%S")

        for sid, sname in STOCK_MAP.items():
            # 使用 fast_info 獲取即時數據 (效能最快)
            tick = yf.Ticker(sid)
            info = tick.fast_info
            
            price = info.last_price
            open_p = info.open
            high_p = info.day_high
            low_p = info.day_low
            
            # 判斷是否為收盤時間 (13:30 之後)
            # 如果還沒到收盤，close_p 給 0.0 避免 SQL NULL 報錯
            is_closing = (now.hour == 13 and now.minute >= 30) or (now.hour > 13)
            close_p = price if is_closing else 0.0

            # SQL 插入語法 (排除 id 與 created_at，讓 SQL 自動生成)
            sql = """
                INSERT INTO dbo.stock_yahoo (sid, sname, price, open_p, close_p, high_p, low_p)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(sql, (sid, sname, price, open_p, close_p, high_p, low_p))
        
        conn.commit()
        print(f"[{current_time_str}] 成功更新 {list(STOCK_MAP.keys())} 的資料至 SQL")

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        if conn:
            conn.close()

# --- 主程式迴圈 ---
if __name__ == "__main__":
    print("===== 股票自動監控系統啟動 =====")
    
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        weekday = now.weekday()  # 0=周一, 6=周日

        # 1. 判斷是否為台股交易時間 (09:00 ~ 13:31) 且為周一至周五
        if "09:00" <= current_time <= "13:31" and weekday <= 4:
            fetch_and_save()
            time.sleep(6)  # 每 6 秒執行一次
        
        # 2. 如果剛過 13:31，進入長休息直到隔天開盤
        elif current_time > "13:31" or weekday > 4:
            print(f"目前時間 {current_time} 為休市時段，系統進入休眠...")
            time.sleep(600)  # 每 10 分鐘檢查一次即可
        
        # 3. 開盤前的等待時間
        else:
            print(f"等待開盤中... 目前時間: {current_time}")
            time.sleep(60)