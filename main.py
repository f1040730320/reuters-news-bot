import requests
import os
import json

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# 使用 rss2json 中繼解析 AP RSS
rss_api_url = "https://api.rss2json.com/v1/api.json?rss_url=https://apnews.com/rss/apf-intlnews"

headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(rss_api_url, headers=headers)
res.encoding = "utf-8"

results = []

try:
    data = res.json()
    data = res.json()
print("Fetched JSON from rss2json:")
print(json.dumps(data, indent=2, ensure_ascii=False))
    for item in data.get("items", []):
        title = item.get("title", "")
        link = item.get("link", "")
        pub_date = item.get("pubDate", "")
        description = item.get("description", "")

        combined_text = f"{title} {description}".lower()
        results.append({
    "title": title,
    "link": link,
    "date": pub_date,
    "content": description
})
except Exception as e:
    print("Parsing error:", e)

# 傳送到 n8n Webhook
if WEBHOOK_URL:
    print("Results to be sent:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    resp = requests.post(WEBHOOK_URL, json=results)
    print(f"POST to n8n status: {resp.status_code}")
else:
    print("WEBHOOK_URL not set.")
