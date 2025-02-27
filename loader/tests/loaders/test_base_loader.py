import pytest
from unittest.mock import MagicMock

from fs_access.base_fs_access import BaseFSAccess

from loaders.base_loader import BaseLoader


class MockLoader(BaseLoader):
    def create_writer(self):
        return MagicMock()


@pytest.fixture
def mock_fs_access() -> MagicMock:
    mock_fs = MagicMock(spec=BaseFSAccess)
    mock_fs.get_file_paths.return_value = ["test1.json", "test2.json"]
    mock_file_1 = MagicMock()
    mock_file_2 = MagicMock()
    mock_file_1.__enter__.return_value = mock_file_1
    mock_file_2.__enter__.return_value = mock_file_2
    mock_file_1.read.return_value = '{"key": "value1"}'
    mock_file_2.read.return_value = '{"key": "value2"}'
    mock_fs.open.side_effect = [mock_file_1, mock_file_2]
    return mock_fs


@pytest.fixture
def mock_loader() -> MagicMock:
    loader = MockLoader()
    loader.create_writer = MagicMock()
    return loader


def test_load_json(mock_fs_access, mock_loader):
    loader = mock_loader
    writer_mock = loader.create_writer()
    loader.load_json(mock_fs_access)

    mock_fs_access.get_file_paths.assert_called_once_with(
        directory="", file_type="json"
    )
    assert mock_fs_access.open.call_count == 2
    writer_mock.write_json.assert_called()
