import json
import urllib.parse
from crawler import get_news
from analyzer import analyze_titles
from slack_sdk.webhook import WebhookClient

def send_slack_message(message: str):
    webhook_url = "https://hooks.slack.com/services/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"
    webhook = WebhookClient(webhook_url)
    response = webhook.send(text=message)
    if response.status_code != 200:
        print("⚠️ Slack 메시지 전송 실패:", response.body)

def main():
    with open("../config/tickers.json") as f:
        tickers = json.load(f)["tickers"]

    full_message = "📊 오늘의 종목별 뉴스 분석 결과\n\n"
    for item in tickers:
        news = get_news(item["keyword"])
        print(f"[{item['name']}] 뉴스 크롤링 결과:")
        for n in news:
            print(f"  - {n['title']}")
        sentiment = analyze_titles(news)
        decision = "🔼 매수" if sentiment["positive"] >= 3 else "⏸ 관망"
        encoded_keyword = urllib.parse.quote(item["keyword"])
        news_url = f"https://news.google.com/rss/search?q={encoded_keyword}+when:1d&hl=ko&gl=KR&ceid=KR:ko"
        full_message += f"✅ <{news_url}|{item['name']}> — {decision}\n"
        full_message += f"긍정: {sentiment['positive']} / 부정: {sentiment['negative']}\n\n"
    send_slack_message(full_message)

if __name__ == "__main__":
    main()
