from typing import Any
from unittest.mock import patch, ANY

from storage.local_storage import LocalStorage
import pytest


@pytest.fixture
def local_storage() -> LocalStorage:
    return LocalStorage()


@pytest.mark.parametrize(
    "data", [1, True, 1.0, {"key1", 2, "key2", "val2"}, [1, 4, {"key1": 2}]]
)
def test_save(local_storage: LocalStorage, data: Any) -> None:
    file_path = "mock_file_path"
    with (
        patch("src.storage.local_storage.json.dump") as mock_json_dump,
        patch("builtins.open") as mock_open,
    ):
        local_storage.save(file_path, data)
        # assert context manager called in write mode
        mock_open.assert_called_once_with(file_path, "w")

        # assert context manager correctly entered and exited
        mock_open.return_value.__enter__.assert_called_once()
        mock_open.return_value.__exit__.assert_called_once()

        # assert json dump to save file called with correct values
        mock_json_dump.assert_called_once_with(
            data, mock_open.return_value.__enter__.return_value, indent=ANY
        )
