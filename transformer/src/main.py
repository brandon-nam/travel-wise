from fs_access.local_fs_access.local_fs_access import LocalFSAccess
from transformers.reddit_transformer.reddit_transformer import RedditTransformer


def main() -> None:
    transformer = RedditTransformer(
        LocalFSAccess(src_directory="raw_data", target_directory="transformed_data")
    )
    transformer.transform()


if __name__ == "__main__":
    main()
