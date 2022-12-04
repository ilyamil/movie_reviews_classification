from datetime import datetime
from typing import Union
from collections.abc import Iterable
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
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
    session: Session,
    model_name: Union[str, Iterable[str]],
    model_version: Union[int, Iterable[int]],
    model_desc: Union[str, Iterable[str]],
    model_ref: Union[str, Iterable[str]],
    train_size: Union[int, Iterable[int]],
    trained_at_dt: Union[datetime, Iterable[datetime]]
):
    args = [
        model_name,
        model_version,
        model_desc,
        model_ref,
        train_size,
        trained_at_dt
    ]
    if all(
            isinstance(arg, Iterable) and not isinstance(arg, str)
            for arg in args
            ):
        records = []
        for nm, ver, desc, ref, size, dt in zip(*args):
            record = Model(
                model_name=nm,
                model_version=ver,
                model_desc=desc,
                model_ref=ref,
                train_size=size,
                trained_at_dt=dt
            )
            records.append(record)
        session.add_all(records)
        session.commit()
    elif all(
            not isinstance(arg, Iterable) or isinstance(arg, str)
            for arg in args
            ):
        records = Model(
            model_name=model_name,
            model_version=model_version,
            model_desc=model_desc,
            model_ref=model_ref,
            train_size=train_size,
            trained_at_dt=trained_at_dt
        )
        session.add(records)
        session.commit()
    else:
        raise ValueError(
            'All arguments (except session) must be either iterable or not'
            ' iterable at the same time. Mixes of iterable and not iterable'
            ' are not supported.'
        )
