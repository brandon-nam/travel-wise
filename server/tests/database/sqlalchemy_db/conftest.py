import pytest
from flask import Flask
from flask_sqlalchemy.session import Session

from src.database.sqlalchemy_db.sqlalchemy_db import SQLAlchemyDB, db
from src.main import create_app


@pytest.fixture(scope="module")
def sqlalchemy_db() -> SQLAlchemyDB:
    # in memory sqlite db for testing purposes
    return SQLAlchemyDB("sqlite:///:memory:")


@pytest.fixture(scope="module")
def test_app(sqlalchemy_db: SQLAlchemyDB) -> Flask:
    app = create_app(sqlalchemy_db)
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def db_session(test_app: Flask) -> Session:
    with test_app.app_context(), db.engine.connect() as connection:
        with connection.begin():
            db.drop_all()
            db.create_all()
            session = db.session
            yield session
            session.rollback()
