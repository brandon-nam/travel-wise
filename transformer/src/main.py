import logging

from fs_access.local_fs_access.local_fs_access import LocalFSAccess

from src.transformers.reddit.comment.reddit_comment_transformer import (
    RedditCommentTransformer,
)
from src.transformers.reddit.post.reddit_post_transformer import RedditPostTransformer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    fs_access = LocalFSAccess()
    post_transformer = RedditPostTransformer(fs_access)
    logger.info(
        f"Running RedditPostTransformer, with handler chain {[step.__class__.__name__ for step in post_transformer.chain]}"
    )
    post_transformer.transform()
    comment_transformer = RedditCommentTransformer(fs_access)
    logger.info(
        f"Running RedditCommentTransformer, with handler chain {[step.__class__.__name__ for step in comment_transformer.chain]}"
    )
    comment_transformer.transform()


if __name__ == "__main__":
    main()
