from typing import List
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sentiment_analysis.database.base import Base


class Prediction(Base):
    __tablename__ = 'prediction'
    prediction_id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('model.model_id'))
    tweet_id = Column(Integer, ForeignKey('tweet.tweet_id'))
    label = Column(String)
    score = Column(Float)
    calculated_at_dt = Column(DateTime)


def add_prediction(
    session,
    prediction_id: List[int],
    model_id: List[int],
    tweet_id: List[int],
    label: List[str],
    score: List[float]
):
    pass
