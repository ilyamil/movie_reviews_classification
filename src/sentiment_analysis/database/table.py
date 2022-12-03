from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'tweet'
    tweet_id = Column(Integer, primary_key=True)
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


class Prediction(Base):
    __tablename__ = 'prediction'
    prediction_id = Column(Integer)
    model_id = Column(Integer, ForeignKey('model.model_id'))
    tweet_id = Column(Integer, ForeignKey('tweet.tweet_id'))
    label = Column(String)
    score = Column(Float)
    calculated_at_dt = Column(DateTime)


class Model(Base):
    __tablename__ = 'model'
    model_id = Column(Integer, primary_key=True)
    model_name = Column(String)
    model_version = Column(Integer)
    model_desc = Column(String)
    model_ref = Column(String)
    train_size = Column(Integer)
    trained_at_dt = Column(DateTime)
