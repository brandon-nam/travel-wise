import os
from unittest.mock import patch, MagicMock

import pytest


from src.main import main, get_pg_connection_uri


def test_main() -> None:
    mock_loader = MagicMock()
    mock_pg_uri = "mock_uri"
    mock_fs_access = MagicMock()

    with (
        patch("src.main.SQLAlchemyLoader") as mock_sqlalchemy_loader,
        patch("src.main.get_pg_connection_uri", return_value=mock_pg_uri),
        patch("src.main.LocalFSAccess") as mock_local_fs_access,
    ):

        mock_sqlalchemy_loader.return_value = mock_loader
        mock_local_fs_access.return_value = mock_fs_access
        main()
        mock_sqlalchemy_loader.assert_called_once_with(mock_pg_uri)
        mock_loader.load_json.assert_called_once_with(mock_fs_access)


@pytest.mark.parametrize(
    "env_vars, expected_uri",
    [
        ({}, "postgresql://postgres:@localhost:5432/cs3203-db"),
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
            "postgresql://postgres:@remote_host:5432/cs3203-db",
        ),
        (
            {"DB_USER": "admin", "DB_PASSWORD": "secret"},
            "postgresql://admin:secret@localhost:5432/cs3203-db",
        ),
    ],
)
def test_get_pg_connection_uri(env_vars: dict[str, str], expected_uri: str) -> None:
    with patch.dict(os.environ, env_vars, clear=True):
        assert get_pg_connection_uri() == expected_uri
