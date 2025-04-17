
import requests
from bs4 import BeautifulSoup
import json
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

search_url = "https://www.reuters.com/site-search/?query=Taiwan+China"
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(search_url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

articles = soup.select("div.search-result-content")
results = []

for a in articles[:5]:
    title_tag = a.select_one("h3.search-result-title > a")
    if not title_tag:
        continue

    title = title_tag.text.strip()
    link = "https://www.reuters.com" + title_tag["href"]

    article_res = requests.get(link, headers=headers)
    article_soup = BeautifulSoup(article_res.text, "html.parser")
    content = " ".join(p.text for p in article_soup.select("div.article-body__content p"))
    pub_time = article_soup.select_one("time")
    pub_date = pub_time["datetime"] if pub_time else "N/A"

    results.append({
        "title": title,
        "link": link,
        "content": content[:500],
        "date": pub_date
    })

# 傳送到 n8n Webhook
if WEBHOOK_URL:
    resp = requests.post(WEBHOOK_URL, json=results)
    print(f"POST to n8n status: {resp.status_code}")
else:
    print("WEBHOOK_URL not set.")
