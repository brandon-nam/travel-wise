from unittest.mock import MagicMock
from src.transformers.reddit.comment.reddit_comment_transformer import (
    RedditCommentTransformer,
    HANDLERS,
)
from fs_access.base_fs_access import BaseFSAccess


def test_reddit_comment_transformer_properties():
    mock_fs = MagicMock(spec=BaseFSAccess)
    transformer = RedditCommentTransformer(mock_fs)

    assert transformer.chain == HANDLERS
    assert transformer.prefix == "comments_"
