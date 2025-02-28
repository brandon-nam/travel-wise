import os

from fs_access.local_fs_access.local_fs_access import LocalFSAccess

from src.extractors.base_extractor import BaseExtractor


class LocalFSExtractor(BaseExtractor):
    def __init__(self, src_dir: str, dest_dir: str, file_type: str):
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.file_type = file_type
        self.fs_access = LocalFSAccess()

    def extract(self):
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)

        src_file_paths = self.fs_access.get_file_paths(self.src_dir, self.file_type)
        for src_file_path in src_file_paths:
            filename = os.path.basename(src_file_path)
            new_file_path = os.path.join(self.dest_dir, filename)
            with (
                self.fs_access.open(src_file_path) as src_file,
                self.fs_access.open(new_file_path, "w") as dest_file,
            ):
                dest_file.write(src_file.read())
