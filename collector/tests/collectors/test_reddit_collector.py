import pytest
from unittest.mock import patch, MagicMock
from src.collectors.reddit_collector import RedditCollector


@pytest.fixture
def mock_reddit_instance():
    mock_reddit = MagicMock()
    mock_reddit.subreddit.return_value.hot.return_value = []
    return mock_reddit


@pytest.fixture
def mock_fetch_hot_posts():
    with patch.object(RedditCollector, "fetch_hot_posts", return_value=[]):
        yield


def test_reddit_collector_init(mock_reddit_instance):
    subreddit_list = ["python", "learnpython"]
    query_limit = 5

    with patch("praw.Reddit", return_value=mock_reddit_instance):
        collector = RedditCollector(
            subreddit_list=subreddit_list, query_limit=query_limit
        )

        assert collector.subreddit_list == subreddit_list
        assert collector.query_limit == query_limit
        assert collector.reddit == mock_reddit_instance


def test_collect(mock_reddit_instance, mock_fetch_hot_posts):
    subreddit_list = ["python"]
    query_limit = 2

    with patch("praw.Reddit", return_value=mock_reddit_instance):
        collector = RedditCollector(
            subreddit_list=subreddit_list, query_limit=query_limit
        )

        mock_reddit_instance.subreddit.return_value.hot.return_value = [
            MagicMock(
                id="abc123",
                title="Test Post",
                url="http://example.com",
                score=10,
                comments=[],
            )
        ]
        collected = list(collector.collect())

        assert len(collected) == 1
        assert collected[0][0].startswith("python_")
        assert collected[0][0].endswith(".json")
        assert isinstance(collected[0][1], list)


def test_fetch_hot_posts(mock_reddit_instance):
    subreddit_name = "python"
    limit = 5

    with patch("praw.Reddit", return_value=mock_reddit_instance):
        posts = RedditCollector.fetch_hot_posts(
            mock_reddit_instance, subreddit_name, limit
        )
        assert isinstance(posts, list)


def test_fetch_comments_from_post(mock_reddit_instance):
    post = MagicMock()
    post.comments.list.return_value = [
        MagicMock(id="comment1", body="This is a comment", score=5)
    ]
    comments = RedditCollector.fetch_comments_from_post(post)

    assert isinstance(comments, list)
    assert len(comments) == 1
    assert comments[0]["id"] == "comment1"
    assert comments[0]["body"] == "This is a comment"
    assert comments[0]["score"] == 5
