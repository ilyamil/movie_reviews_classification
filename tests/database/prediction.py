import os
from sentiment_analysis.database.base import Base
from sentiment_analysis.database.prediction import Prediction, add_prediction
from sentiment_analysis.database.model import Model
from sentiment_analysis.database.tweet import Tweet
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


def test_create_prediction_table():
    Base.metadata.create_all(ENGINE, checkfirst=True)
    insp = inspect(ENGINE)
    assert Prediction.__tablename__ in insp.get_table_names()


def test_dummy():
    path = os.path.abspath(DATABASE['database'])
    os.remove(path)
