import pytest
from flask import Flask
from flask_sqlalchemy.session import Session

from src.database.sqlalchemy_db.sqlalchemy_db import SQLAlchemyDB
from src.database.sqlalchemy_db.sqlalchemy_models import db
from src.main import create_app


@pytest.fixture(scope="module")
def test_app() -> Flask:
    app = create_app(SQLAlchemyDB("sqlite:///:memory:"))
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function")
def db_session(test_app: Flask) -> Session:
    with test_app.app_context(), db.engine.connect() as connection:
        with connection.begin():
            session = db.session
            yield session
            session.rollback()
