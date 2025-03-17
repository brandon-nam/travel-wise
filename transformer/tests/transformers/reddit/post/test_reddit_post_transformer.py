from unittest.mock import MagicMock
from src.transformers.reddit.post.reddit_post_transformer import (
    RedditPostTransformer,
    HANDLERS,
)
from fs_access.base_fs_access import BaseFSAccess


def test_reddit_comment_transformer_properties():
    mock_fs = MagicMock(spec=BaseFSAccess)
    transformer = RedditPostTransformer(mock_fs)

    assert transformer.chain == HANDLERS
    assert transformer.prefix == "posts_"
