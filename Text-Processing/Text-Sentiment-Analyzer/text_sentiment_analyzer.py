"""
This program contains functions for performing Natural Language Processing (NLP).
"""

import nltk
nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(TEXT):
    SIA = SentimentIntensityAnalyzer()
    SENTIMENT_SCORES = SIA.polarity_scores(TEXT)
    
    if SENTIMENT_SCORES['compound'] >= 0.05:
        SENTIMENT = "Positive"
    elif SENTIMENT_SCORES['compound'] <= -0.05:
        SENTIMENT = "Negative"
    else:
        SENTIMENT = "Neutral"
    
    print(f"Text: {TEXT}")
    print(f"Sentiment Scores: {SENTIMENT_SCORES}")
    print(f"Overall Sentiment: {SENTIMENT}")
    
    return SENTIMENT_SCORES, SENTIMENT
