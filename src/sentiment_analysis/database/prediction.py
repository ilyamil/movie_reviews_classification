from typing import List, Union, Iterable
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sentiment_analysis.database.base import Base


class Prediction(Base):
    __tablename__ = 'prediction'
    prediction_id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('model.model_id'))
    tweet_id = Column(Integer, ForeignKey('tweet.tweet_id'))
    label = Column(String)
    score = Column(Float)


def add_prediction(
    session,
    model_id: Union[List[int], int],
    tweet_id: Union[List[int], int],
    label: Union[List[str], str],
    score: Union[List[float], float]
):
    args = [model_id, tweet_id, label, score]
    if all(
            isinstance(arg, Iterable) and not isinstance(arg, str)
            for arg in args
            ):
        existed_prediction = (
            session.query(Prediction)
            .filter(
                Prediction.model_id.in_(model_id),
                Prediction.tweet_id.in_(tweet_id)
            )
            .all()
        )
        existed_prediction_ = {
            (el.model_id, el.tweet_id, el.label, el.score)
            for el in existed_prediction
        }
        already_added = set()
        records = set()
        for mid, tid, l, s in zip(*args):
            if (mid, tid, l, s) in existed_prediction_\
               or (mid, tid, l, s) in already_added:
                continue

            record = Prediction(model_id=mid, tweet_id=tid, label=l, score=s)
            records.add(record)
            already_added.add(record)

        if len(records) > 0:
            session.add_all(records)
            session.commit()
    elif all(
            not isinstance(arg, Iterable) or isinstance(arg, str)
            for arg in args
            ):
        existed_prediction = (
            session.query(Prediction)
            .filter(
                Prediction.model_id == model_id,
                Prediction.tweet_id == tweet_id
            )
            .all()
        )
        if len(existed_prediction) == 0:
            record = Prediction(
                model_id=model_id,
                tweet_id=tweet_id,
                label=label,
                score=score
            )
            session.add(record)
            session.commit()
    else:
        raise ValueError(
            'All arguments (except session) must be either iterable or not'
            ' iterable at the same time. Mixes of iterable and not iterable'
            ' are not supported.'
        )
