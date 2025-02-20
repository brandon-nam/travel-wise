import datetime
import logging
import os
from typing import Any, Generator

import praw
from dotenv import load_dotenv
from praw import Reddit
from praw.models import Submission

from collectors.collector import Collector

logger = logging.getLogger(__name__)


class RedditCollector(Collector):
    def __init__(self, subreddit_list: list[str], query_limit: int) -> None:
        self.subreddit_list = subreddit_list
        self.query_limit = query_limit
        load_dotenv()
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="collector",
        )

    def collect(self) -> Generator[tuple[str, list], None, None]:
        for subreddit_name in self.subreddit_list:
            logger.info(
                f"Attempting to fetch data from subreddit r/{subreddit_name}..."
            )
            posts = RedditCollector.fetch_hot_posts(
                reddit=self.reddit,
                subreddit_name=subreddit_name,
                limit=self.query_limit,
            )
            logger.info(
                f"Successfully fetched {len(posts)} posts and "
                f"{sum(len(post['comments']) for post in posts)} comments from r/{subreddit_name}..."
            )
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            file_path = f"{subreddit_name}_{current_date}.json"
            yield file_path, posts

    @staticmethod
    def fetch_hot_posts(
        reddit: Reddit, subreddit_name: str, limit: int
    ) -> list[dict[str, Any]]:
        subreddit = reddit.subreddit(subreddit_name)
        posts = [
            {
                "title": post.title,
                "id": post.id,
                "url": post.url,
                "score": post.score,
                "comments": RedditCollector.fetch_comments_from_post(post),
            }
            for post in subreddit.hot(limit=limit)
        ]
        return posts

    @staticmethod
    def fetch_comments_from_post(post: Submission) -> list[dict[str, Any]]:
        post.comments.replace_more(limit=0)
        return [
            {
                "id": comment.id,
                "body": comment.body,
                "score": comment.score,
            }
            for comment in post.comments.list()
        ]
