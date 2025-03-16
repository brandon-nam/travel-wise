import pytest
import os
import datetime
from unittest.mock import MagicMock
from src.collectors.reddit_collector import RedditCollector


@pytest.fixture
def mock_reddit():
    mock_reddit = MagicMock()
    mock_subreddit = MagicMock()
    mock_reddit.subreddit.return_value = mock_subreddit
    return mock_reddit


@pytest.fixture
def reddit_collector(mock_reddit):
    os.environ["REDDIT_CLIENT_ID"] = "dummy_client_id"
    os.environ["REDDIT_CLIENT_SECRET"] = "dummy_client_secret"

    collector = RedditCollector(subreddit_list=["test_subreddit"], query_limit=10)
    collector.reddit = mock_reddit
    return collector


def test_collect(reddit_collector, mock_reddit):
    original_fetch_hot_posts_and_comments = RedditCollector.fetch_hot_posts_and_comments
    original_save_data_paginated = RedditCollector.save_data_paginated
    mock_posts = [{"title": "Post 1", "id": "1", "url": "url1", "score": 10}]
    mock_comments = [{"id": "c1", "body": "Comment 1", "score": 5, "post_id": "1"}]
    mock_save_data_paginated = MagicMock()

    RedditCollector.fetch_hot_posts_and_comments = MagicMock(
        return_value=(mock_posts, mock_comments)
    )
    RedditCollector.save_data_paginated = mock_save_data_paginated

    list(reddit_collector.collect())

    assert mock_save_data_paginated.call_count == 2

    RedditCollector.fetch_hot_posts_and_comments = original_fetch_hot_posts_and_comments
    RedditCollector.save_data_paginated = original_save_data_paginated


def test_save_data_paginated():
    test_data = [{"id": "1", "body": "Test comment", "score": 5, "post_id": "1"}] * 100
    subreddit_name = "test_subreddit"
    result = list(
        RedditCollector.save_data_paginated(subreddit_name, test_data, "comments")
    )
    assert len(result) == 4
    assert (
        result[0][0]
        == f"comments_test_subreddit_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}_page_1.json"
    )


def test_fetch_hot_posts_and_comments(mock_reddit):
    mock_post = MagicMock()
    mock_post.title = "Valid Post"
    mock_post.id = "1"
    mock_post.url = "http://example.com"
    mock_post.score = 10
    mock_post.is_gallery = False
    mock_post.comments.list.return_value = [
        MagicMock(id="c1", body="Test comment", score=5)
    ]
    mock_subreddit = MagicMock()
    mock_subreddit.hot.return_value = [mock_post]
    mock_reddit.subreddit.return_value = mock_subreddit
    posts, comments = RedditCollector.fetch_hot_posts_and_comments(
        mock_reddit, "test_subreddit", 10
    )
    assert len(posts) == 1
    assert len(comments) == 1


def test_fetch_comments_from_post():
    mock_post = MagicMock()
    mock_comment = MagicMock(id="c1", body="Test comment", score=5)
    mock_post.comments.list.return_value = [mock_comment]

    comments = RedditCollector.fetch_comments_from_post(mock_post)
    assert len(comments) == 1
    assert comments[0]["id"] == "c1"
    assert comments[0]["body"] == "Test comment"
    assert comments[0]["score"] == 5
    assert comments[0]["post_id"] == mock_post.id
