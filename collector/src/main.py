import json
import logging

from fs_access.local_fs_access.local_fs_access import LocalFSAccess

from collectors.reddit_collector import RedditCollector

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

COLLECTORS = [
    RedditCollector(subreddit_list=["KoreaTravel", "JapanTravel"], query_limit=3)
]


def main():
    fs_access = LocalFSAccess()
    for collector in COLLECTORS:
        logger.info(f"Begin: Collecting from {collector.__class__.__name__}")
        file_paths = []
        for file_path, data in collector.collect():
            file_paths.append(file_path)
            with fs_access.open(file_path, "w") as f:
                json.dump(data, f, indent=4)
        logger.info(
            f"Successfully saved {len(file_paths)} files using {fs_access.__class__.__name__}: {file_paths}"
        )


if __name__ == "__main__":
    main()
