import json
from crawler import get_news
from analyzer import analyze_titles
from notifier import send_slack_message

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
        full_message += f"✅ {item['name']} — {decision}\n"
        full_message += f"긍정: {sentiment['positive']} / 부정: {sentiment['negative']}\n\n"
    send_slack_message(full_message)

if __name__ == "__main__":
    main()
