from sentiment_analysis.database.base import Base
from sentiment_analysis.database.model import Model
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker


DB_URL = 'sqlite:///test.db'
ENGINE = create_engine(DB_URL)
SESSION = sessionmaker(bind=ENGINE)


def test_create_model_table():
    Base.metadata.create_all(ENGINE, checkfirst=True)
    insp = inspect(ENGINE)
    assert Model.__tablename__ in insp.get_table_names()
