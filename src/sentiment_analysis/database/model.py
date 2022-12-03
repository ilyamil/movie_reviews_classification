from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sentiment_analysis.database.base import Base


class Model(Base):
    __tablename__ = 'model'
    model_id = Column(Integer, primary_key=True)
    model_name = Column(String)
    model_version = Column(Integer)
    model_desc = Column(String)
    model_ref = Column(String)
    train_size = Column(Integer)
    trained_at_dt = Column(DateTime)


def add_model(
    session,
    model_name: str,
    model_version: int,
    model_desc: str,
    model_ref: str,
    train_size: int,
    trained_at_dt: datetime
):
    pass
