from unittest.mock import patch, mock_open
import os

from fs_access.local_fs_access.local_fs_access import LocalFSAccess


def test_get_file_paths():
    local_fs_access = LocalFSAccess()

    with patch("glob.glob") as mock_glob:
        mock_glob.return_value = ["file1.txt", "file2.txt"]
        result = local_fs_access.get_file_paths("/some/directory", "txt")
        assert result == ["file1.txt", "file2.txt"]
        mock_glob.assert_called_once_with(
            os.path.join("/some/directory", "**", "*.txt"), recursive=True
        )


def test_open():
    local_fs_access = LocalFSAccess()

    mock_file = mock_open(read_data="File content")

    with patch("builtins.open", mock_file):
        with local_fs_access.open("some/file.txt", "r") as f:
            content = f.read()
            assert content == "File content"
            mock_file.assert_called_once_with("some/file.txt", "r")
