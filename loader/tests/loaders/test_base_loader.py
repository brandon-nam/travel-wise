import pytest
from unittest.mock import MagicMock, patch

from fs_access.base_fs_access import BaseFSAccess

from loaders.base_loader import BaseLoader


class MockLoader(BaseLoader):
    def create_writer(self):
        return MagicMock()


@pytest.fixture
def mock_fs_access() -> MagicMock:
    mock_fs = MagicMock(spec=BaseFSAccess)
    mock_fs.get_file_paths.return_value = [
        "comments_test1.json",
        "posts_test2.json",
        "test3.json",
    ]
    mock_file_1 = MagicMock()
    mock_file_2 = MagicMock()
    mock_file_1.__enter__.return_value = mock_file_1
    mock_file_2.__enter__.return_value = mock_file_2
    mock_file_1.read.return_value = '{"key": "value1"}'
    mock_file_2.read.return_value = '{"key": "value2"}'
    mock_fs.open.side_effect = [mock_file_1, mock_file_2]
    return mock_fs


@pytest.fixture
def mock_loader() -> MockLoader:
    loader = MockLoader()
    loader.create_writer = MagicMock()
    loader._write = MagicMock()
    return loader


def test_load_json(mock_fs_access, mock_loader):
    loader = mock_loader
    mock_write_func = MagicMock()
    with patch.object(mock_loader, "write", mock_write_func):
        loader.load_json(mock_fs_access)
        mock_fs_access.get_file_paths.assert_called_once_with(
            directory="", file_type="json"
        )
        assert mock_write_func.call_count == 2


def test_write(mock_fs_access, mock_loader):
    mock_file_path = "comments_test4.json"
    loader = mock_loader
    mock_write_func = MagicMock()
    mock_json_data = {"comment": "test4"}
    with patch("src.loaders.base_loader.json.load") as mock_load:
        mock_load.return_value = mock_json_data
        loader.write(mock_fs_access, mock_file_path, mock_write_func)
        mock_load.assert_called_once()
        mock_fs_access.open.assert_called_once_with(mock_file_path)
        mock_write_func.assert_called_once_with(mock_json_data)
