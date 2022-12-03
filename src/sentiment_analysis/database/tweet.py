from typing import List
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sentiment_analysis.database.base import Base


class Tweet(Base):
    __tablename__ = 'tweet'
    tweet_id = Column(Integer, primary_key=True, autoincrement=False)
    author_id = Column(Integer)
    text = Column(String)
    retweet_count = Column(Integer)
    reply_count = Column(Integer)
    like_count = Column(Integer)
    quote_count = Column(Integer)
    created_at_dt = Column(DateTime)
    start_dt = Column(DateTime)
    end_dt = Column(DateTime)
    loaded_at_dt = Column(DateTime)


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
