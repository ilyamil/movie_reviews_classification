import tweepy
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any


def load_tweets(
    token: str,
    user_id: List[int],
    max_results: int,
    start_dt: datetime,
    end_dt: datetime
) -> Dict[str, List[Any]]:
    client = tweepy.Client(token)
    users_tweets = []
    for uid in user_id:
        response = client.get_users_tweets(
            uid,
            max_results=max_results,
            start_time=start_dt,
            end_time=end_dt,
            tweet_fields=['public_metrics', 'created_at']
        )
        if not response.data:
            continue

        tweets_ = pd.DataFrame({
            'user_id': [uid]*len(response.data),
            'tweet_id': [tweet.id for tweet in response.data],
            'text': [tweet.text for tweet in response.data],
            'created_at': [tweet.created_at for tweet in response.data],
            'public_metrics': [tweet.public_metrics for tweet in response.data]
        })
        tweets = (
            tweets_
            .join(tweets_['public_metrics'].apply(pd.Series))
            .drop(['public_metrics'], axis=1)
        )
        users_tweets.append(tweets)
    return pd.concat(users_tweets)
