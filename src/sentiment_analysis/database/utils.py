from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def create_session(url: str, engine) -> Session:
    engine = create_engine(url)
    session = sessionmaker(bind=engine)
    return session
