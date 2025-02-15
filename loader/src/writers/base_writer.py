from abc import ABC, abstractmethod
from typing import Any


class BaseWriter(ABC):
    @abstractmethod
    def write_json(self, json_data: dict[str, Any]) -> None:
        pass
