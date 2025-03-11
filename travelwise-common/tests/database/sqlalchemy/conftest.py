import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from database.sqlalchemy.models import Base

engine = create_engine("sqlite:///:memory:", echo=False)

SessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Session:
    Base.metadata.create_all(engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
