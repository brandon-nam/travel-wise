import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from database.sqlalchemy.models import Base


@pytest.fixture
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
