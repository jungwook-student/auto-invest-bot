from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("snunlp/KR-FinBert-SC")
model = AutoModelForSequenceClassification.from_pretrained("snunlp/KR-FinBert-SC")
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_title_with_rule(title: str, model_classifier) -> str:
    model_label = model_classifier(title)[0]['label'].lower()

    lower_title = title.lower()
    negative_keywords = ["하락", "적자", "실적 부진", "적자 전환", "악화", "우려",
                         "구조조정", "리스크", "리밸런싱", "매각", "철수", "파산", "소송", "법정관리"]
    positive_keywords = ["상승", "호재", "실적 개선", "흑자", "수혜", "기대",
                         "신제품", "합병", "투자 유치", "해외 진출", "신규 수주", "전망 밝음"]

    if any(word in lower_title for word in negative_keywords):
        return "negative"
    elif any(word in lower_title for word in positive_keywords):
        return "positive"

    return model_label

def analyze_titles(news_list):
    pos, neg = 0, 0
    for news in news_list:
        title = news["title"]
        label = analyze_title_with_rule(title, classifier)
        print(f"[분석] \"{title}\" → {label}")
        if label == 'positive':
            pos += 1
        elif label == 'negative':
            neg += 1
    return {"positive": pos, "negative": neg}
