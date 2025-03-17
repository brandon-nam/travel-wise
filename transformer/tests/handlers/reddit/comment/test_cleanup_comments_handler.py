import pytest
from handlers.reddit.comment.cleanup_comments_handler import (
    CleanupCommentsHandler,
    clean_string,
)


@pytest.fixture
def handler():
    return CleanupCommentsHandler()


def test_clean_string():
    assert clean_string("Hello\\nWorld") == "Hello World"
    assert clean_string("Hello\\tWorld") == "Hello World"
    assert clean_string("Hello\xa0World") == "Hello World"
    assert clean_string("Hello \\u2019 World") == "Hello  World"
