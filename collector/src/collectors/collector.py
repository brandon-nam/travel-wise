from abc import ABC, abstractmethod
from typing import Generator


class Collector(ABC):
    @abstractmethod
    def collect(self) -> Generator[tuple[str, list], None, None]:
        """
        Generator method that yields tuples of (file_path, data), to be saved into storage.
        The data provided must be JSON-serializable python objects.
        """
        pass
