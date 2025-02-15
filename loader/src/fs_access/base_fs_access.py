from abc import ABC, abstractmethod
from typing import IO


class BaseFSAccess(ABC):
    """
    Base FSAccess class, used to obtain files from different filesystems (e.g. local, S3, GCS, etc.)
    """

    @abstractmethod
    def get_file_paths(self, file_type: str) -> list[str]:
        # file_type without the dot (.) e.g. get_file_paths("json") or get_file_paths("csv")
        pass

    @abstractmethod
    def open(self, path: str) -> IO:
        # needs to be a context manager (handle cleanup/closing of file after reading)
        pass
