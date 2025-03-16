import datetime
import logging
import os
from typing import Any, Generator

import praw
from dotenv import load_dotenv
from praw import Reddit
from praw.models import Submission

from src.collectors.collector import Collector

logger = logging.getLogger(__name__)
BATCH_SIZE = 25


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
            posts, comments = RedditCollector.fetch_hot_posts_and_comments(
                reddit=self.reddit,
                subreddit_name=subreddit_name,
                limit=self.query_limit,
            )

            yield from RedditCollector.save_data_paginated(
                subreddit_name, posts, "posts"
            )
            yield from RedditCollector.save_data_paginated(
                subreddit_name, comments, "comments"
            )
            logger.info(
                f"Saving {len(posts)} posts and "
                f"{len(comments)} comments from r/{subreddit_name}..."
            )

    @staticmethod
    def save_data_paginated(
        subreddit_name: str, data: list, prefix: str
    ) -> Generator[tuple[str, list], None, None]:
        for page_number, i in enumerate(range(0, len(data), BATCH_SIZE), start=1):
            batch_comments = data[i : i + BATCH_SIZE]
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            file_path = (
                f"{prefix}_{subreddit_name}_{current_date}_page_{page_number}.json"
            )
            yield file_path, batch_comments

    @staticmethod
    def fetch_hot_posts_and_comments(
        reddit: Reddit, subreddit_name: str, limit: int
    ) -> tuple[list, list]:
        subreddit = reddit.subreddit(subreddit_name)
        all_posts = []
        all_comments = []
        for post in subreddit.hot(limit=limit):
            if "meet-up" in post.title.lower() or "meetup" in post.title.lower():
                continue
            comments = RedditCollector.fetch_comments_from_post(post)
            if len(comments) > 0 and not getattr(post, "is_gallery", False):
                all_posts.append(
                    {
                        "title": post.title,
                        "id": post.id,
                        "url": post.url,
                        "score": post.score,
                    }
                )
                all_comments.extend(comments)

        return all_posts, all_comments

    @staticmethod
    def fetch_comments_from_post(post: Submission) -> list[dict[str, Any]]:
        post.comments.replace_more(limit=0)
        return [
            {
                "id": comment.id,
                "body": comment.body,
                "score": comment.score,
                "post_id": post.id,
            }
            for comment in post.comments.list()
        ]
