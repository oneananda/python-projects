"""
This program contains functions for performing Natural Language Processing (NLP).
"""

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using VADER sentiment analysis.

    Parameters:
    text (str): The text to analyze.

    Returns:
    tuple: A tuple containing the sentiment scores dictionary and the overall sentiment as a string.
    """
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    if sentiment_scores['compound'] >= 0.05:
        sentiment = "Positive"
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    print(f"Text: {text}")
    print(f"sentiment Scores: {sentiment_scores}")
    print(f"Overall sentiment: {sentiment}")
    return sentiment_scores, sentiment
# Positive
# text = "I'm so happy with this product! It's amazing and works perfectly."
TEXT = "I'm not happy with this product! It's not amazing and works imperfectly."
SENTIMENT_SCORES, SENTIMENT = analyze_sentiment(TEXT)
print(SENTIMENT_SCORES)
print(SENTIMENT)
