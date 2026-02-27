# src/analysis/news_sentiment.py
import random

from monitoring import data_logger

def get_fake_news_sentiment(symbol):
    """Fake news fetch + sentiment – in real version: use NewsAPI or scrape"""
    # Simulate: 70% neutral, 15% positive, 15% negative
    rand = random.random()
    if rand < 0.15:
        score = random.uniform(0.3, 0.8)   # positive
        sentiment = "positive"
    elif rand < 0.30:
        score = random.uniform(-0.8, -0.3) # negative
        sentiment = "negative"
    else:
        score = random.uniform(-0.2, 0.2)  # neutral
        sentiment = "neutral"

    logger.debug(f"Fake news sentiment for {symbol}: {sentiment} ({score:.2f})")
    return score