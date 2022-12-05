import os
from sentiment_analysis.database.base import Base
from sentiment_analysis.database.prediction import Prediction, add_prediction
from sentiment_analysis.database.model import Model # noqa
from sentiment_analysis.database.tweet import Tweet # noqa
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


DATABASE = {
    'drivername': 'sqlite',
    'database': 'test.db'
}
ENGINE = create_engine(URL.create(**DATABASE))
SESSION = sessionmaker(bind=ENGINE)()


def test_create_prediction_table():
    Base.metadata.create_all(ENGINE, checkfirst=True)
    insp = inspect(ENGINE)
    assert Prediction.__tablename__ in insp.get_table_names()


def test_add_prediction_single_record():
    record = {
        'model_id': 1,
        'tweet_id': 1,
        'label': 'positive',
        'score': 0.99
    }
    add_prediction(SESSION, **record)
    q = SESSION.query(Prediction).all()
    assert len(q) == 1
    assert (
        (q[0].model_id == record['model_id'])
        & (q[0].tweet_id == record['tweet_id'])
        & (q[0].label == record['label'])
        & (q[0].score == record['score'])
    )


def test_add_prediction_single_record_twice():
    record = {
        'model_id': 2,
        'tweet_id': 1,
        'label': 'positive',
        'score': 0.99
    }
    add_prediction(SESSION, **record)
    add_prediction(SESSION, **record)
    q = (
        SESSION.query(Prediction)
        .filter(Prediction.model_id == record['model_id'])
        .all()
    )
    assert len(q) == 1


def test_add_prediction_multiple_records_same():
    record = {
        'model_id': [1, 1],
        'tweet_id': [1, 1],
        'label': ['positive', 'positive'],
        'score': [0.99, 0.99]
    }
    add_prediction(SESSION, **record)
    q = (
        SESSION.query(Prediction)
        .filter(Prediction.model_id == 1)
        .all()
    )
    assert len(q) == 1


def test_add_prediction_multiple_records_different():
    record = {
        'model_id': [3, 3],
        'tweet_id': [10, 20],
        'label': ['positive', 'positive'],
        'score': [0.99, 0.99]
    }
    add_prediction(SESSION, **record)
    q = (
        SESSION.query(Prediction)
        .filter(Prediction.model_id == 3)
        .all()
    )
    assert len(q) == 2


def test_dummy():
    path = os.path.abspath(DATABASE['database'])
    os.remove(path)
