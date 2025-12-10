# ⏰ 定時任務測試資料

這個資料夾包含用於練習建立定時任務的範例程式和設定檔。

---

## 📁 資料夾結構

### examples/
包含各種定時任務的範例程式：

1. **daily_report.py** - 每日報表生成（即將建立）
2. **backup_task.py** - 自動備份任務（即將建立）
3. **monitor.py** - 網頁監控任務（即將建立）

### setup_scripts/
包含各平台的排程設定腳本：

1. **windows_schedule.ps1** - Windows 工作排程器設定
2. **schedule_python.py** - Python schedule 套件範例

### config/
排程設定檔案：

1. **schedule_config.json** - 任務設定檔

---

## 🎯 練習建議

### 初級練習：簡單定時任務
```
用 Copilot Chat 說：
「建立一個 Python 腳本
 每天早上 9 點自動執行
 生成 Excel 報表」
```

### 中級練習：監控任務
```
「建立一個價格監控腳本
 每小時檢查一次商品價格
 價格變動時發送通知」
```

### 高級練習：完整自動化系統
```
「建立一個每日摘要系統
 週一到週五早上 8:30
 自動收集數據、生成報表、寄送郵件」
```

---

## ⏰ Windows 工作排程器設定步驟

### 方法 1：使用 GUI
1. 開啟「工作排程器」（搜尋 Task Scheduler）
2. 點擊「建立基本工作」
3. 輸入名稱和描述
4. 選擇觸發條件（每天、每週等）
5. 設定執行時間
6. 選擇「啟動程式」
7. 瀏覽選擇 Python 執行檔和腳本

### 方法 2：使用 PowerShell
```powershell
# 建立每日 9:00 執行的任務
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\path\to\script.py"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "DailyReport"
```

---

## 🐍 Python schedule 套件範例

```python
import schedule
import time

def job():
    print("執行任務...")
    # 你的任務程式碼

# 設定排程
schedule.every().day.at("09:00").do(job)  # 每天 9:00
schedule.every().hour.do(job)              # 每小時
schedule.every().monday.at("08:30").do(job) # 每週一 8:30
schedule.every(10).minutes.do(job)         # 每 10 分鐘

# 持續執行
while True:
    schedule.run_pending()
    time.sleep(60)  # 每分鐘檢查一次
```

---

## 🔧 Cron 格式說明（Linux/Mac）

```bash
# 分 時 日 月 週 指令
# *  *  *  *  *

# 範例：
0 9 * * * python /path/to/script.py        # 每天 9:00
0 */2 * * * python script.py               # 每 2 小時
30 8 * * 1 python script.py                # 每週一 8:30
0 0 1 * * python script.py                 # 每月 1 號 0:00
*/15 * * * * python script.py              # 每 15 分鐘
```

---

## 📊 設定檔範例（JSON）

```json
{
  "tasks": [
    {
      "name": "daily_report",
      "script": "daily_report.py",
      "schedule": "09:00",
      "enabled": true
    },
    {
      "name": "backup",
      "script": "backup_task.py",
      "schedule": "23:00",
      "enabled": true
    }
  ]
}
```

---

## 🛡️ 最佳實踐

### 1. 日誌記錄
```python
import logging

logging.basicConfig(
    filename='task.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

logging.info("任務開始")
# 執行任務
logging.info("任務完成")
```

### 2. 錯誤處理
```python
try:
    execute_task()
except Exception as e:
    logging.error(f"錯誤：{e}")
    send_alert(e)
```

### 3. 鎖定機制
```python
import os

lock_file = 'task.lock'
if os.path.exists(lock_file):
    print("任務正在執行中")
    exit()

# 建立鎖定檔
open(lock_file, 'w').close()

try:
    execute_task()
finally:
    os.remove(lock_file)
```

---

記住：**好的定時任務系統讓工作自動化！** ⏰
