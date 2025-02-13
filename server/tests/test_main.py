import os
from unittest.mock import patch, MagicMock

import pytest

from src.main import main, create_app, get_pg_connection_uri


def test_main() -> None:
    mock_app = MagicMock()
    with patch("src.main.create_app") as mock_create_app_func:
        mock_create_app_func.return_value = mock_app
        main()
        mock_create_app_func.assert_called_once()
        mock_app.run.assert_called_once_with(host="0.0.0.0", port=3203)


def test_create_app() -> None:
    mock_app = MagicMock()
    mock_pg_uri = "mock_uri"
    mock_db = MagicMock()
    with (
        patch("src.main.__name__") as mock_name,
        patch("src.main.Flask") as mock_flask,
        patch("src.main.CORS") as mock_cors,
        patch("src.main.SQLAlchemyDB") as mock_sqlalchemy,
        patch("src.main.get_pg_connection_uri") as mock_get_pg_uri,
        patch("src.main.create_routes") as mock_create_routes,
    ):
        mock_flask.return_value = mock_app
        mock_get_pg_uri.return_value = mock_pg_uri
        mock_sqlalchemy.return_value = mock_db
        returned_app = create_app()
        mock_flask.assert_called_once_with(mock_name)
        mock_cors.assert_called_once_with(mock_app)
        mock_sqlalchemy.assert_called_once_with(mock_app, mock_pg_uri)
        mock_db.setup_db.assert_called_once()
        mock_create_routes.assert_called_once_with(mock_app, mock_db)
        assert returned_app == mock_app


@pytest.mark.parametrize(
    "env_vars, expected_uri",
    [
        ({}, "postgresql://postgres:@localhost:5432/travelwise"),
        (
            {
                "DB_HOST": "db.example.com",
                "DB_PORT": "5433",
                "DB_USER": "user",
                "DB_PASSWORD": "pass",
                "DB_NAME": "testdb",
            },
            "postgresql://user:pass@db.example.com:5433/testdb",
        ),
        (
            {"DB_HOST": "remote_host"},
            "postgresql://postgres:@remote_host:5432/travelwise",
        ),
        (
            {"DB_USER": "admin", "DB_PASSWORD": "secret"},
            "postgresql://admin:secret@localhost:5432/travelwise",
        ),
    ],
)
def test_get_pg_connection_uri(env_vars: dict[str, str], expected_uri: str) -> None:
    with patch.dict(os.environ, env_vars, clear=True):
        assert get_pg_connection_uri() == expected_uri
