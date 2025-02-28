from unittest.mock import patch

from src.main import main


def test_main():
    with patch("src.main.LocalFSExtractor") as mock_local_fs_extractor_class:
        mock_extractor_instance = mock_local_fs_extractor_class.return_value
        main()
        mock_local_fs_extractor_class.assert_called_once_with(
            src_dir="", dest_dir="extracted_data", file_type="json"
        )
        mock_extractor_instance.extract.assert_called_once()
