import logging
from unittest.mock import MagicMock, patch

import pytest
from _pytest.logging import LogCaptureFixture

from src.main import main


@pytest.fixture
def mock_fs_access() -> MagicMock:
    with patch("src.main.LocalFSAccess") as MockFS:
        mock_fs = MockFS.return_value
        mock_fs.open = MagicMock()
        yield mock_fs


@pytest.fixture
def mock_collector() -> MagicMock:
    with patch("src.main.RedditCollector") as MockCollector:
        mock_collector = MockCollector.return_value
        mock_collector.collect.return_value = [
            ("file1.json", {"data": "test1"}),
            ("file2.json", {"data": "test2"}),
        ]
        yield mock_collector


def test_main(
    mock_fs_access: MagicMock, mock_collector: MagicMock, caplog: LogCaptureFixture
):
    with patch("src.main.COLLECTORS", [mock_collector]):
        caplog.set_level(logging.INFO)

        main()

        mock_collector.collect.assert_called_once()

        assert mock_fs_access.open.call_count == 2
        expected_calls = [
            ("file1.json", "w"),
            ("file2.json", "w"),
        ]
        actual_calls = [call[0] for call in mock_fs_access.open.call_args_list]
        print(actual_calls, expected_calls)
        assert actual_calls == expected_calls

        for call in mock_fs_access.open.call_args_list:
            file_handle = call[0][1]
            assert file_handle == "w"

        assert "Begin: Collecting from MagicMock" in caplog.text
        assert "Successfully saved 2 files using MagicMock" in caplog.text
