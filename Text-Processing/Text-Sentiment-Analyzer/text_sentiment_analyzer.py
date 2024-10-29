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
    SIA = SentimentIntensityAnalyzer()
    sentiment_scores = SIA.polarity_scores(text)
    if sentiment_scores['compound'] >= 0.05:
        SENTIMENT = "Positive"
    elif sentiment_scores['compound'] <= -0.05:
        SENTIMENT = "Negative"
    else:
        SENTIMENT = "Neutral"
    print(f"Text: {text}")
    print(f"Sentiment Scores: {sentiment_scores}")
    print(f"Overall Sentiment: {SENTIMENT}")
    return sentiment_scores, SENTIMENT
