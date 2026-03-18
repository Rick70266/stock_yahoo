"""
提供排成的方式固定在 9:00 ~ 13:00 分執行，每30秒執行一次
第二 單次執行( 13:31 分) 執行一次
pip install schedule
"""

import schedule
import time
from datetime import datetime

def run_every_10_seconds():
    print("每 10 秒執行一次")

def run_every_60_seconds():
    print("每 60 秒執行一次")

def run_at_spec_time():
    now = datetime.now()
    print(f"觸發時間:{now}")

def run_and_cancelJob():
    # 本任務視情況,決定是否繼續執行,例如各分點的檔案在營業結束後要上傳 pos csv file
    cnt = True
    if (cnt):
        return schedule.cancel_job  # 回傳 CancelJob 就會取消這個任務,不再執行)


# 只是安排一個任務
# schedule.every(10).seconds.do(run_every_10_seconds)
# schedule.every(1).minutes.do(run_every_60_seconds)
# schedule.every().day.at("14:12").do(run_at_spec_time)
# schedule.every().hour.at(":12").do()
# schedule.every().friday.at("16:25").do()

# 隨機一種數值執行處發
schedule.every(3).to(10).seconds.do(run_at_spec_time) # 每 3~10 秒執行一次


# 設定結束或取消的方式
schedule.every(30).seconds.do(run_every_10_seconds).until("15:30") #開始每30秒執行任務 直到13:30結束
schedule.every().hours.at(":50").do(run_and_cancelJob) #一旦檔案下載完成 自動結束


while True:
    schedule.run_pending()  # 要求 schedule 每n個單位 檢查一次是否有任務需要執行
    time.sleep(1)  # 等待 1 秒後再次檢查是否有任務需要執行