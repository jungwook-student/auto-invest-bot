from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import feedparser
from urllib.parse import quote
from urllib.request import Request, urlopen
import ssl

def get_news(keyword: str, max_articles=10):
    encoded_keyword = quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}+when:1d&hl=ko&gl=KR&ceid=KR:ko"

    context = ssl._create_unverified_context()
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, context=context) as response:
        data = response.read()

    feed = feedparser.parse(data)
    print(f"[{keyword}] RSS 피드 수신: {len(feed.entries)}건")
    return [{"title": entry.title, "url": entry.link} for entry in feed.entries[:max_articles]]
