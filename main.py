import requests
import xml.etree.ElementTree as ET
import os
import json

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

rss_url = "https://feeds.reuters.com/Reuters/worldNews"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(rss_url, headers=headers)
res.encoding = "utf-8"

results = []

try:
    root = ET.fromstring(res.text)
    for item in root.findall(".//item"):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")
        description = item.findtext("description", "")

        combined_text = f"{title} {description}".lower()
        if any(keyword in combined_text for keyword in ["台灣", "中國", "taiwan", "china"]):
            results.append({
                "title": title,
                "link": link,
                "date": pub_date,
                "content": description
            })
except Exception as e:
    print("Failed to parse RSS:", e)

# 傳送給 n8n Webhook
if WEBHOOK_URL:
    print("Results to be sent:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    resp = requests.post(WEBHOOK_URL, json=results)
    print(f"POST to n8n status: {resp.status_code}")
else:
    print("WEBHOOK_URL not set.")
