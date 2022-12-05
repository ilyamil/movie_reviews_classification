import os
from sentiment_analysis.database.base import Base
from sentiment_analysis.database.model import Model, add_model
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
    assert Model.__tablename__ in insp.get_table_names()


def test_add_model_single_record():
    record = {
        'model_name': 'logreg',
        'model_version': 1,
        'model_desc': 'some desc',
        'model_ref': 'here.joblib',
        'train_size': 1,
        'trained_at_dt': datetime(2000, 1, 31)
    }
    add_model(SESSION, **record)
    records = SESSION.query(Model).all()
    assert len(records) == 1
    assert (
        (records[0].model_id == 1)
        & (records[0].model_name == record['model_name'])
        & (records[0].model_version == record['model_version'])
        & (records[0].model_desc == record['model_desc'])
        & (records[0].model_ref == record['model_ref'])
        & (records[0].train_size == record['train_size'])
        & (records[0].trained_at_dt == record['trained_at_dt'])
    )


def test_add_model_single_record_twice():
    record = {
        'model_name': 'logreg',
        'model_version': 2,
        'model_desc': 'some desc',
        'model_ref': 'here.joblib',
        'train_size': 1,
        'trained_at_dt': datetime(2000, 1, 31)
    }
    add_model(SESSION, **record)
    record = {
        'model_name': 'logreg',
        'model_version': 2,
        'model_desc': 'some desc',
        'model_ref': 'here.joblib',
        'train_size': 1,
        'trained_at_dt': datetime(2000, 1, 31)
    }
    add_model(SESSION, **record)
    records_back = SESSION.query(Model).filter(Model.model_version == 2).all()
    assert len(records_back) == 1


def test_add_model_multiple_records_same():
    records = {
        'model_name': ['logreg', 'logreg'],
        'model_version': [3, 3],
        'model_desc': ['some desc', 'some desc'],
        'model_ref': ['here.joblib', 'here.joblib'],
        'train_size': [1, 1],
        'trained_at_dt': [datetime(2000, 1, 31), datetime(2000, 1, 31)]
    }
    Base.metadata.create_all(ENGINE, checkfirst=True)
    add_model(SESSION, **records)
    records_back = (
        SESSION.query(Model)
        .filter(Model.model_version == 3)
        .all()
    )
    assert len(records_back) == 1


def test_add_model_multiple_records_different():
    records = {
        'model_name': ['logreg', 'logreg_tfidf'],
        'model_version': [4, 4],
        'model_desc': ['some desc', 'some desc'],
        'model_ref': ['here.joblib', 'here.joblib'],
        'train_size': [1, 1],
        'trained_at_dt': [datetime(2000, 1, 31), datetime(2000, 1, 31)]
    }
    Base.metadata.create_all(ENGINE, checkfirst=True)
    add_model(SESSION, **records)
    records_back = (
        SESSION.query(Model)
        .filter(Model.model_version == 4)
        .all()
    )
    assert len(records_back) == 2


def test_dummy():
    path = os.path.abspath(DATABASE['database'])
    os.remove(path)
