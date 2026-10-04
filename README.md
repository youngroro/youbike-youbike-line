# YouBike 即時資訊 LINE 通知

使用 Python 定時擷取「臺北市 YouBike 2.0 即時資訊」Open Data，透過 JSONPath 取得指定租借站點的可借車與可還車數量，並使用 LINE Messaging API 將結果發送至 LINE。

## 功能

- 使用 Requests 擷取 YouBike 2.0 Open Data
- 使用 JSONPath 搜尋指定 YouBike 站點
- 顯示可借車數量及可還車數量
- 可借車數量過低時加入警告訊息
- 使用 LINE Messaging API 發送通知
- 使用 Python Schedule 每日定時執行
- 預設每日 09:00 發送 YouBike 即時資訊

## 使用技術

- Python 3
- Requests
- JSONPath-NG
- Schedule
- Python Dotenv
- LINE Messaging API
- 臺北市資料大平臺 Open Data

## 程式流程

```text
臺北市 YouBike Open Data
          ↓
       Requests
          ↓
        JSON
          ↓
      JSONPath
          ↓
   搜尋指定 YouBike 站點
          ↓
取得可借車數 / 可還車數
          ↓
      條件判斷
          ↓
   LINE Messaging API
          ↓
      LINE 手機通知
```

## 專案結構

```text
open-data-line/
├── .env.example
├── .gitignore
├── line_test.py
├── main.py
├── README.md
└── requirements.txt
```

`.env` 用來保存 LINE Messaging API 的相關設定，因此不會上傳至 GitHub。

## 安裝

### 1. Clone 專案

```bash
git clone git@github.com:youngroro/youbike-youbike-line.git
cd youbike-youbike-line
```

### 2. 建立虛擬環境

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安裝套件

```bash
pip install -r requirements.txt
```

## 環境變數設定

在專案根目錄建立 `.env`：

```env
LINE_CHANNEL_ACCESS_TOKEN=你的_LINE_CHANNEL_ACCESS_TOKEN
LINE_USER_ID=你的_LINE_USER_ID
```

請勿將 `.env` 上傳至 GitHub，以避免 LINE Channel Access Token 外洩。

## 執行方式

```bash
python main.py
```

程式啟動後會持續執行，並於每日：

```text
09:00
```

自動取得指定 YouBike 站點的最新資訊並發送 LINE 訊息。

> 程式必須保持執行狀態，若程式關閉、電腦關機或 WSL 停止執行，排程將不會執行。

## LINE 通知範例

```text
🚲 YouBike 每日即時資訊
站點：YouBike2.0_捷運科技大樓站
可借車數：2
可還車數：24
更新時間：2026-10-03 15:48:03
⚠️ 可借車數量偏低，建議確認後再前往
```

當可借車數量小於或等於 3 台時，系統會自動加入警告訊息。

## Open Data

本專案使用「YouBike2.0 臺北市公共自行車即時資訊」。

主要使用欄位：

| 欄位 | 說明 |
| --- | --- |
| `sna` | YouBike 站點名稱 |
| `available_rent_bikes` | 可借車數量 |
| `available_return_bikes` | 可還車位數量 |
| `mday` | 資料更新時間 |

## 排程

本專案使用 `schedule` 套件：

```python
schedule.every().day.at("09:00").do(check_youbike)
```

並持續檢查是否有待執行的排程：

```python
while True:
    schedule.run_pending()
    time.sleep(1)
```

因此每日 09:00 會自動執行 YouBike 資料查詢及 LINE 通知。