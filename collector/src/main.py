from collectors.reddit_collector import RedditCollector
from storage.local_storage import LocalStorage

COLLECTOR_CLASSES = [RedditCollector]


def main():
    storage = LocalStorage()
    for collector_class in COLLECTOR_CLASSES:
        collector = collector_class()
        for file_path, data in collector.collect():
            storage.save(file_path=file_path, data=data)


if __name__ == "__main__":
    main()
