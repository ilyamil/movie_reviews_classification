import os
from sentiment_analysis.database.base import Base
from sentiment_analysis.database.tweet import Tweet, add_tweet
from datetime import datetime
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


DATABASE = {
    'drivername': 'sqlite',
    'database': 'test.db'
}
ENGINE = create_engine(URL.create(**DATABASE))
SESSION = sessionmaker(bind=ENGINE)()


def test_create_model_table():
    Base.metadata.create_all(ENGINE, checkfirst=True)
    insp = inspect(ENGINE)
    assert Tweet.__tablename__ in insp.get_table_names()


def test_add_tweet_single_record():
    record = {
        'tweet_id': 111,
        'author_id': 1,
        'text': 'abc',
        'retweet_count': 100,
        'reply_count': 100,
        'like_count': 100,
        'quote_count': 100,
        'created_at_dt': datetime(2020, 1, 31),
        'start_dt': datetime(2020, 1, 31),
        'end_dt': datetime(2022, 1, 31)
    }
    add_tweet(SESSION, **record)
    records = SESSION.query(Tweet).all()
    assert len(records) == 1
    assert (
        (records[0].tweet_id == record['tweet_id'])
        & (records[0].author_id == record['author_id'])
        & (records[0].text == record['text'])
        & (records[0].retweet_count == record['retweet_count'])
        & (records[0].reply_count == record['reply_count'])
        & (records[0].like_count == record['like_count'])
        & (records[0].quote_count == record['quote_count'])
        & (records[0].created_at_dt == record['created_at_dt'])
        & (records[0].start_dt == record['start_dt'])
        & (records[0].end_dt == record['end_dt'])
    )


def test_add_tweet_multiple_records_same():
    record = {
        'tweet_id': [111, 111],
        'author_id': [1, 1],
        'text': ['abc', 'abc'],
        'retweet_count': [100, 100],
        'reply_count': [100, 100],
        'like_count': [100, 100],
        'quote_count': [100, 100],
        'created_at_dt': [datetime(2020, 1, 31), datetime(2020, 1, 31)],
        'start_dt': [datetime(2020, 1, 31), datetime(2020, 1, 31)],
        'end_dt': [datetime(2020, 1, 31), datetime(2022, 1, 31)]
    }
    add_tweet(SESSION, **record)
    records_back = SESSION.query(Tweet).all()
    assert len(records_back) == 1


def test_add_tweet_multiple_records_different():
    record = {
        'tweet_id': [111, 122],
        'author_id': [1, 1],
        'text': ['abc', 'abc'],
        'retweet_count': [100, 100],
        'reply_count': [100, 100],
        'like_count': [100, 100],
        'quote_count': [100, 100],
        'created_at_dt': [datetime(2020, 1, 31), datetime(2020, 1, 31)],
        'start_dt': [datetime(2020, 1, 31), datetime(2020, 1, 31)],
        'end_dt': [datetime(2020, 1, 31), datetime(2022, 1, 31)]
    }
    add_tweet(SESSION, **record)
    records_back = SESSION.query(Tweet).all()
    assert len(records_back) == 2


def test_dummy():
    path = os.path.abspath(DATABASE['database'])
    os.remove(path)
