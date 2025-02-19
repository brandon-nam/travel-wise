from fs_access.local_fs_access.local_fs_access import LocalFSAccess
from transformers.reddit_transformer import RedditTransformer


def main() -> None:
    transformer = RedditTransformer(LocalFSAccess(""))
    transformer.transform()


if __name__ == "__main__":
    main()
