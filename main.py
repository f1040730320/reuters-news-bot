import feedparser
import os
import requests
import json

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RSS_URL = "https://rss2json.com/api.json?rss_url=https://apnews.com/rss"

feed = feedparser.parse(RSS_URL)

results = []
for entry in feed.entries[:10]:
    title = entry.title
    link = entry.link
    pub_date = entry.published
    description = entry.summary if hasattr(entry, "summary") else ""

    results.append({
        "title": title,
        "link": link,
        "date": pub_date,
        "content": description,
        "source": "AP"
    })

if WEBHOOK_URL and results:
    print("✅ Sending AP news to Webhook:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    requests.post(WEBHOOK_URL, json=results)
else:
    print("⚠️ No articles or WEBHOOK_URL not set.")

