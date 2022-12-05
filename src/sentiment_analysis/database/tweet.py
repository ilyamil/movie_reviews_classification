from typing import List
from datetime import datetime
from collections.abc import Iterable
from sqlalchemy import Column, Integer, String, DateTime
from sentiment_analysis.database.base import Base


class Tweet(Base):
    __tablename__ = 'tweet'
    tweet_id = Column(
        Integer,
        primary_key=True,
        autoincrement=False,
        unique=True
    )
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


def add_tweet(
    session,
    tweet_id: List[int],
    author_id: List[int],
    text: List[str],
    retweet_count: List[int],
    reply_count: List[int],
    like_count: List[int],
    quote_count: List[int],
    created_at_dt: List[datetime],
    start_dt: List[datetime],
    end_dt: List[datetime]
):
    args = [
        tweet_id,
        author_id,
        text,
        retweet_count,
        reply_count,
        like_count,
        quote_count,
        created_at_dt,
        start_dt,
        end_dt
    ]
    if all(
            isinstance(arg, Iterable) and not isinstance(arg, str)
            for arg in args
            ):
        existed_tweet_id = (
            session
            .query(Tweet)
            .filter(Tweet.tweet_id.in_(tweet_id))
            .all()
        )
        existed_tweet_id_ = {tw.tweet_id for tw in existed_tweet_id}
        records = []
        for twid, aid, t, rtwc, rpc, lkc, qc, cad, sd, ed in zip(*args):
            if twid in existed_tweet_id_:
                continue
            record = Tweet(
                tweet_id=twid,
                author_id=aid,
                text=t,
                retweet_count=rtwc,
                reply_count=rpc,
                like_count=lkc,
                quote_count=qc,
                created_at_dt=cad,
                start_dt=sd,
                end_dt=ed
            )
            records.append(record)
        session.add_all(records)
        session.commit()
    elif all(
            not isinstance(arg, Iterable) or isinstance(arg, str)
            for arg in args
            ):
        records = Tweet(
            tweet_id=tweet_id,
            author_id=author_id,
            text=text,
            retweet_count=retweet_count,
            reply_count=reply_count,
            like_count=like_count,
            quote_count=quote_count,
            created_at_dt=created_at_dt,
            start_dt=start_dt,
            end_dt=end_dt
        )
        session.add(records)
        session.commit()
    else:
        raise ValueError(
            'All arguments (except session) must be either iterable or not'
            ' iterable at the same time. Mixes of iterable and not iterable'
            ' are not supported.'
        )
