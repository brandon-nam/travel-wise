import json
from unittest.mock import MagicMock, patch
from src.transformers.reddit.reddit_transformer import RedditTransformer
from fs_access.base_fs_access import BaseFSAccess
from src.handlers.base_handler import BaseHandler


def test_reddit_transformer_init():

    mock_handlers = [MagicMock(spec=BaseHandler) for _ in range(8)]

    chain_property = property(lambda self: mock_handlers)
    prefix_property = property(lambda self: "test")

    with patch.object(RedditTransformer, "chain", chain_property):
        with patch.object(RedditTransformer, "prefix", prefix_property):
            mock_fs = MagicMock(spec=BaseFSAccess)
            transformer = RedditTransformer(mock_fs)

            assert isinstance(transformer.chain, list)
            assert len(transformer.chain) == 8
            for handler in transformer.chain:
                assert isinstance(handler, BaseHandler)


@patch("os.path.exists")
@patch("os.makedirs")
def test_transform(mock_makedirs, mock_exists):

    mock_handler = MagicMock(spec=BaseHandler)
    mock_handler.handle.return_value = json.dumps([{"transformed": True}])

    chain_property = property(lambda self: [mock_handler])
    prefix_property = property(lambda self: "test")

    with patch.object(RedditTransformer, "chain", chain_property):
        with patch.object(RedditTransformer, "prefix", prefix_property):
            mock_fs_access = MagicMock(spec=BaseFSAccess)
            transformer = RedditTransformer(mock_fs_access)

            mock_fs_access.get_file_paths.return_value = ["raw_data/test_post.json"]
            mock_exists.return_value = False

            mock_file_content = json.dumps(
                [
                    {
                        "title": "Best travel tips?",
                        "body": "Should I visit Paris in summer?",
                    }
                ]
            )

            mock_file = MagicMock()
            mock_fs_access.open.return_value.__enter__.return_value = mock_file

            def get_content(*args, **kwargs):
                return mock_file_content

            mock_file.read.side_effect = get_content

            transformer.transform()

            mock_makedirs.assert_called_once_with("transformed_data")
            mock_handler.handle.assert_called_once()
            mock_fs_access.open.assert_any_call("raw_data/test_post.json")
            mock_fs_access.open.assert_any_call("transformed_data/test_post.json", "w")
