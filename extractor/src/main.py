from src.extractors.local_fs_extractor.local_fs_extractor import LocalFSExtractor


def main():
    extractor = LocalFSExtractor(
        src_dir="", dest_dir="extracted_data", file_type="json"
    )
    extractor.extract()


if __name__ == "__main__":
    main()
