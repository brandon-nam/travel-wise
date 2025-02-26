import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from writers.sqlalchemy_writer.sqlalchemy_models import Base


@pytest.fixture(scope="function")
def db_uri() -> str:
    return "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session(db_uri: str):
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    yield session

    session.rollback()
    session.close()
    engine.dispose()
