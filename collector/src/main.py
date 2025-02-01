import logging

from collectors.reddit_collector import RedditCollector
from storage.local_storage import LocalStorage

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

COLLECTORS = [
    RedditCollector(subreddit_list=["askSingapore", "JapanTravel"], query_limit=3)
]


def main():
    storage = LocalStorage()
    for collector in COLLECTORS:
        logger.info(f"Begin: Collecting from {collector.__class__.__name__}")
        file_paths = []
        for file_path, data in collector.collect():
            file_paths.append(file_path)
            storage.save(file_path=file_path, data=data)
        logger.info(
            f"Successfully saved {len(file_paths)} files using {storage.__class__.__name__}: {file_paths}"
        )


if __name__ == "__main__":
    main()
