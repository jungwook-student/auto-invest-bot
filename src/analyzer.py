from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("snunlp/KR-FinBert-SC")
model = AutoModelForSequenceClassification.from_pretrained("snunlp/KR-FinBert-SC")
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_titles(news_list):
    pos, neg = 0, 0
    for news in news_list:
        title = news["title"]
        result = classifier(title)[0]
        label = result['label'].lower()
        if label == 'positive':
            pos += 1
        elif label == 'negative':
            neg += 1
    return {"positive": pos, "negative": neg}
