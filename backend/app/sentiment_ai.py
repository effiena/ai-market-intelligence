from transformers import pipeline

# Load ONCE globally (not inside functions)
_sentiment_pipeline = None


def get_model():
    global _sentiment_pipeline

    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="ProsusAI/finbert"
        )

    return _sentiment_pipeline


def analyze_sentiment(text):
    model = get_model()
    result = model(text)[0]

    label = result["label"].lower()
    score = round(result["score"] * 100, 2)

    if label == "positive":
        sentiment = "bullish"
        impact = "positive market impact"
    elif label == "negative":
        sentiment = "bearish"
        impact = "negative market pressure"
    else:
        sentiment = "neutral"
        impact = "uncertain market reaction"

    return {
        "sentiment": sentiment,
        "confidence": score,
        "impact": impact
    }
