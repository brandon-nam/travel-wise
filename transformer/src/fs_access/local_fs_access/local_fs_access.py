import glob
import os
from contextlib import contextmanager
from typing import IO

from src.fs_access.base_fs_access import BaseFSAccess


class LocalFSAccess(BaseFSAccess):
    def __init__(self, src_directory: str, target_directory: str):
        self.src_directory = src_directory
        self.target_directory = target_directory
        os.makedirs(self.target_directory, exist_ok=True)

    def get_src_file_paths(self, file_type: str) -> list[str]:
        return glob.glob(
            os.path.join(self.src_directory, "**", f"*.{file_type.lower()}"),
            recursive=True,
        )

    def get_transformed_file_path(self, file_path: str) -> str:
        return os.path.join(self.target_directory, os.path.basename(file_path))

    @contextmanager
    def open(self, path: str, mode: str = "r") -> IO:
        with open(path, mode) as f:
            yield f
