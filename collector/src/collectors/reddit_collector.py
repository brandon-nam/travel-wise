import datetime
import os
from typing import Any, Generator

import praw
from dotenv import load_dotenv
from praw.models import Submission

from collectors.collector import Collector


SUBREDDITS_TO_COLLECT_FROM = ["askSingapore", "JapanTravel"]
QUERY_LIMIT = 3


class RedditCollector(Collector):
    def __init__(self) -> None:
        load_dotenv()
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent="collector",
        )

    def collect(self) -> Generator[tuple[str, list], None, None]:
        for subreddit_name in SUBREDDITS_TO_COLLECT_FROM:
            posts = self.fetch_hot_posts(
                subreddit_name=subreddit_name, limit=QUERY_LIMIT
            )
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            file_path = f"{subreddit_name}_{current_date}.json"
            yield file_path, posts

    def fetch_hot_posts(self, subreddit_name: str, limit: int) -> list[dict[str, Any]]:
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        for post in subreddit.hot(limit=limit):
            posts.append(
                {
                    "title": post.title,
                    "id": post.id,
                    "url": post.url,
                    "score": post.score,
                    "comments": fetch_comments_from_post(post),
                }
            )
        return posts


def fetch_comments_from_post(post: Submission) -> list[dict[str, Any]]:
    post.comments.replace_more(limit=0)
    comments = []

    for comment in post.comments.list():
        comments.append(
            {"id": comment.id, "body": comment.body, "score": comment.score}
        )

    return comments
