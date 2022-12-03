from datetime import datetime
from typing import List


def add_tweets(
    session,
    tweet_id: List[int],
    author_id: List[int],
    text: List[str],
    retweet_count: List[int],
    reply_count: List[int],
    like_count: List[int],
    quote_count: List[int],
    created_at_dt: List[datetime],
    start_dt: datetime,
    end_dt: datetime
):
    pass


def add_predictions(
    session,
    prediction_id: List[int],
    model_id: List[int],
    tweet_id: List[int],
    label: List[str],
    score: List[float]
):
    pass


def add_model(
    session,
    model_name: str,
    model_version: int,
    model_desc: str,
    model_ref: str,
    train_size: int,
    trained_at_dt: datetime
):
    pass
