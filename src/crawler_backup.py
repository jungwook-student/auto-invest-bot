import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def get_news(keyword: str, max_articles=30):
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sort=1&pd=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    
    # 🔍 HTML 구조 확인 로그
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
    
    soup = BeautifulSoup(resp.text, "html.parser")
    news_items = soup.select("a.news_tit")
    results = []
    for item in news_items[:max_articles]:
        results.append({"title": item["title"], "url": item["href"]})
    return results
