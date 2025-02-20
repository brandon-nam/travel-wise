from abc import ABC, abstractmethod
from typing import IO


class BaseFSAccess(ABC):
    """
    Base FSAccess class, used to obtain files from different filesystems (e.g. local, S3, GCS, etc.)
    """

    @abstractmethod
    def get_src_file_paths(self, file_type: str) -> list[str]:
        # file_type without the dot (.) e.g. get_file_paths("json") or get_file_paths("csv")
        raise NotImplementedError()

    @abstractmethod
    def get_transformed_file_path(self, transformed_file_path: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def open(self, path: str, mode: str = "r") -> IO:
        # needs to be a context manager (handle cleanup/closing of file after reading)
        raise NotImplementedError()
