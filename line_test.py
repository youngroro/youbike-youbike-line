import os
import requests
from dotenv import load_dotenv

load_dotenv()

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
user_id = os.getenv("LINE_USER_ID")

url = "https://api.line.me/v2/bot/message/push"

headers = {
    "Authorization": f"Bearer {channel_access_token}",
    "Content-Type": "application/json"
}

data = {
    "to": user_id,
    "messages": [
        {
            "type": "text",
            "text": "🚲 YouBike 測試訊息"
        }
    ]
}

response = requests.post(
    url,
    headers=headers,
    json=data
)

print("status:", response.status_code)
print("response:", response.text)