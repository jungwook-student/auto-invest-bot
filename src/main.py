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
            print(f"  - [{n['source']}] {n['title']}")
        sentiment = analyze_titles(news)
        decision = "🔼 매수" if sentiment["positive"] >= 3 else "⏸ 관망"
        full_message += f"✅ {item['name']} — {decision}\n"
        for i, n in enumerate(news):
            full_message += f"• 출처{i+1} ({n['source']}): <{n['url']}|{n['title'][:30]}...>\n"
        full_message += f"긍정: {sentiment['positive']} / 부정: {sentiment['negative']}\n\n"
    send_slack_message(full_message)

if __name__ == "__main__":
    main()
