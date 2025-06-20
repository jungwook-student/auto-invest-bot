import yfinance as yf

tickers = {
    "삼성전자": "005930.KS",
    "SK스퀘어": "402340.KQ",
    "CJ ENM": "035760.KQ"
}

date = "2025-06-16"
eval_date = "2025-06-19"

for name, code in tickers.items():
    df = yf.download(code, start=date, end="2025-06-20")  # end는 하루 뒤 날짜 필요
    print(f"{name} ({code}) 종가:")
    print(df["Close"])