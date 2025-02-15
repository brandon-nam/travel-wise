import glob
import os
from typing import IO

from src.fs_access.base_fs_access import BaseFSAccess


class LocalFSAccess(BaseFSAccess):
    def __init__(self, directory: str):
        self.directory = directory

    def get_file_paths(self, file_type: str) -> list[str]:
        return glob.glob(
            os.path.join(self.directory, "**", f"*.{file_type.lower()}"), recursive=True
        )

    def open(self, path: str) -> IO:
        return open(path, "r")
