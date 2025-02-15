from abc import ABC, abstractmethod
from typing import IO


class BaseFSAccess(ABC):
    """
    Base FSAccess class, used to obtain files from different filesystems (e.g. local, S3, GCS, etc.)
    """

    @abstractmethod
    def get_json_file_paths(self) -> list[str]:
        pass

    @abstractmethod
    def open(self, path: str) -> IO:
        pass
