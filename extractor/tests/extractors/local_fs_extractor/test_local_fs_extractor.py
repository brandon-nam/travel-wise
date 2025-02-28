from unittest.mock import mock_open, patch, MagicMock
import pytest
from src.extractors.local_fs_extractor.local_fs_extractor import LocalFSExtractor


@pytest.fixture
def mock_fs_access() -> MagicMock:
    with patch(
        "src.extractors.local_fs_extractor.local_fs_extractor.LocalFSAccess"
    ) as MockLocalFSAccess:
        mock_instance = MockLocalFSAccess.return_value
        mock_instance.get_file_paths.return_value = [
            "test_dir/file1.json",
            "test_dir/file2.json",
        ]
        mock_instance.open = mock_open(read_data='{"key": "value"}')
        yield mock_instance


def test_extract(mock_fs_access: MagicMock):
    with (
        patch("os.makedirs") as mock_makedirs,
        patch("os.path.exists", return_value=False),
    ):
        extractor = LocalFSExtractor(
            src_dir="test_dir", dest_dir="dest_dir", file_type="json"
        )
        extractor.extract()

        mock_makedirs.assert_called_once_with("dest_dir")
        mock_fs_access.get_file_paths.assert_called_once_with("test_dir", "json")
        # 1 read and 1 write per file
        assert mock_fs_access.open.call_count == 2 * len(
            mock_fs_access.get_file_paths.return_value
        )

        expected_calls = [
            (("test_dir/file1.json",),),
            (("dest_dir/file1.json", "w"),),
            (("test_dir/file2.json",),),
            (("dest_dir/file2.json", "w"),),
        ]
        actual_calls = mock_fs_access.open.call_args_list
        for expected, actual in zip(expected_calls, actual_calls):
            assert expected == actual
