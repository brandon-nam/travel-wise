from abc import ABC, abstractmethod
from typing import Any


class BaseWriter(ABC):
    @abstractmethod
    def write_posts(self, json_data: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def write_comments(self, json_data: dict[str, Any]) -> None:
        pass
