import pytest
from unittest.mock import MagicMock
from flask import Flask
from src.routes.routes import create_routes


mock_get_posts_resp = b"mocked post response"
mock_get_comments_resp = b"mocked comments response"
mock_get_countries_resp = b"mocked countries response"
mock_get_characteristics_resp = b"mocked characteristics response"


@pytest.fixture
def app():
    app = Flask(__name__)
    repo = MagicMock()
    repo.get_posts.return_value = mock_get_posts_resp
    repo.get_comments.return_value = mock_get_comments_resp
    repo.get_countries.return_value = mock_get_countries_resp
    repo.get_characteristics.return_value = mock_get_characteristics_resp
    create_routes(app, repo)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.parametrize(
    "endpoint, expected_data",
    [
        ("/posts", mock_get_posts_resp),
        ("/comments", mock_get_comments_resp),
        ("/countries", mock_get_countries_resp),
        ("/characteristics", mock_get_characteristics_resp),
    ],
)
def test_get_endpoints(client: MagicMock, endpoint: str, expected_data: bytes) -> None:
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response.data == expected_data
