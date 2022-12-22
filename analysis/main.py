import pandas as pd
import tweetnlp

from typing import Dict, List, Optional, Tuple

def analyse(
    tweet_table: Dict[str, List[str]],
    exclude_handles: Optional[List[str]] = [],
    period: str = "day",
    model: str = "sentiment_multilingual"
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:

    tweet_df = pd.DataFrame(tweet_table)
    tweet_df_filtered = remove_tweets_from_excluded_handles(tweet_df, exclude_handles)

    model_xml = tweetnlp.load(model)

    tweets = pd.DataFrame(tweet_df_filtered.tweet_text)

    sentiments = []
    probabilities = []
    for tweet in tweet_df_filtered.tweet_text:
        prediction = model_xml.predict(tweet)
        sentiments.append(prediction['label'])
        probabilities.append(prediction['probability'])

    tweet_df_filtered["sentiment"] = sentiments
    tweet_df_filtered["probability"] = probabilities

    tweets = tweet_df_filtered[
        [
            'author_id',
            'created_at',
            'tweet_text',
            'sentiment',
            'probability',
            'possibly_sensitive',
            'retweet_count',
            'reply_count',
            'like_count',
            'quote_count',
            'lang',
            'source'
        ]
    ]

    tweets['sentiment'] = tweets['sentiment'].map(
        {
            'negative': -1.0,
            'neutral': 0.0,
            'positive': 1.0
        }
    )

    tweets['sentiment_score_1'] = tweets.sentiment * tweets.probability

    tweets['sentiment_score_2'] = tweets.sentiment * tweets.probability * (tweets.retweet_count + tweets.reply_count + tweets.like_count + tweets.quote_count + 1)

    x = tweets.set_index(pd.DatetimeIndex(tweets.created_at))
    periods = {
        'day': 'D',
    }
    binning_period = periods[period]
    y_1 = x.resample(binning_period).mean().to_dict()
    y_2 = x.resample(binning_period).mean().to_dict()

    return y_1, y_2


def remove_tweets_from_excluded_handles(
    tweets_table: pd.DataFrame,
    excluded_handles: List[str]
) -> pd.DataFrame:
    """Remove tweets from excluded handles from the Tweets table."""
    if excluded_handles:
        tweet_df_filtered = tweets_table[tweets_table.author_id.isin(excluded_handles) is False]
    else:
        tweet_df_filtered = tweets_table
    return tweet_df_filtered
