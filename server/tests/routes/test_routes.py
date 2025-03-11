import pytest
from unittest.mock import MagicMock
from flask import Flask
from src.routes.routes import create_routes


mock_get_posts_resp = b"mocked post response"
mock_get_comments_resp = b"mocked comments response"


@pytest.fixture
def app():
    app = Flask(__name__)
    database = MagicMock()
    database.get_posts.return_value = mock_get_posts_resp
    database.get_comments.return_value = mock_get_comments_resp
    create_routes(app, database)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_posts(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.data == mock_get_posts_resp


def test_get_comments(client):
    response = client.get("/comments")
    assert response.status_code == 200
    assert response.data == mock_get_comments_resp
