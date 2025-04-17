import feedparser
import os
import requests
import json

WEBHOOK_URL = "https://primary-production-f061.up.railway.app/webhook-test/acae2e40-eb14-4a8f-be7d-b3a7d7c45579"
RSS_URL = "https://feeds.reuters.com/reuters/worldNews"

feed = feedparser.parse(RSS_URL)

results = []
for entry in feed.entries[:10]:
    title = entry.title
    link = entry.link
    pub_date = entry.published
    description = entry.summary

    combined_text = f"{title} {description}".lower()
    if "taiwan" in combined_text or "china" in combined_text:
        results.append({
            "title": title,
            "link": link,
            "date": pub_date,
            "content": description,
            "source": "Reuters"
        })

if results:
    print("✅ Sending Reuters news to Webhook:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    requests.post(WEBHOOK_URL, json=results)
else:
    print("⚠️ No matching articles.")
