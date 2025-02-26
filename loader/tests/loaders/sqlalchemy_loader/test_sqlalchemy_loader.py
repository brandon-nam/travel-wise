import pytest

from src.loaders.sqlalchemy_loader.sqlalchemy_loader import SQLAlchemyLoader
from src.writers.sqlalchemy_writer.sqlalchemy_writer import SQLAlchemyWriter


@pytest.fixture
def db_uri() -> str:
    return "mock_db_uri"


@pytest.fixture
def sqlalchemy_loader(db_uri: str) -> SQLAlchemyLoader:
    return SQLAlchemyLoader(db_uri)


def test_create_writer(sqlalchemy_loader: SQLAlchemyLoader, db_uri: str) -> None:
    assert isinstance(sqlalchemy_loader.create_writer(), SQLAlchemyWriter)
