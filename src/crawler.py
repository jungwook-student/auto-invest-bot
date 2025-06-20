from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import feedparser
from urllib.parse import quote
import requests
import xml.etree.ElementTree as ET

def get_yna_news(max_articles=10):
    url = "https://www.yna.co.kr/rss/economy.xml"
    response = requests.get(url)
    articles = []
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for item in root.findall(".//item")[:max_articles]:
            title = item.find("title").text
            link = item.find("link").text
            articles.append({"title": title, "url": link})
    return articles

def get_news(keyword: str, max_articles=10):
    encoded_keyword = quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}+when:1d&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)
    google_articles = [{"title": entry.title, "url": entry.link, "source": "Google"} for entry in feed.entries[:max_articles]]
    yna_articles = [{"title": item["title"], "url": item["url"], "source": "연합뉴스"} for item in get_yna_news(max_articles)]
    return google_articles + yna_articles
