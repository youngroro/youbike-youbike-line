import os
import time
import requests
import schedule
from dotenv import load_dotenv
from jsonpath_ng.ext import parse

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

YOUBIKE_URL = (
    "https://tcgbusfs.blob.core.windows.net/"
    "dotapp/youbike/v2/youbike_immediate.json"
)

STATION_NAME = "YouBike2.0_捷運科技大樓站"


def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=10
    )

    print("LINE status:", response.status_code)
    print("LINE response:", response.text)


def check_youbike():
    print("開始取得 YouBike 即時資料...")

    response = requests.get(
        YOUBIKE_URL,
        timeout=10
    )

    data = response.json()

    jsonpath_expr = parse(
        f"$[?(@.sna == '{STATION_NAME}')]"
    )

    matches = jsonpath_expr.find(data)

    if not matches:
        print("找不到指定站點")
        return

    station = matches[0].value

    rent_bikes = station["available_rent_bikes"]
    return_bikes = station["available_return_bikes"]
    update_time = station["mday"]

    message = (
        f"🚲 YouBike 每日即時資訊\n"
        f"站點：{station['sna']}\n"
        f"可借車數：{rent_bikes}\n"
        f"可還車數：{return_bikes}\n"
        f"更新時間：{update_time}"
    )

    if rent_bikes <= 3:
        message += "\n⚠️ 可借車數量偏低，建議確認後再前往"

    print(message)

    send_line_message(message)


schedule.every().day.at("09:00").do(check_youbike)

print("YouBike 排程程式已啟動")
print("每日 09:00 將自動發送 LINE 訊息")

while True:
    schedule.run_pending()
    time.sleep(1)