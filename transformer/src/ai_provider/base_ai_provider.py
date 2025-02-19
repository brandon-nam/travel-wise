from abc import ABC, abstractmethod
from typing import Any


class BaseAIProvider(ABC):
    @abstractmethod
    def prompt(self, query: str, params: dict[str, Any]) -> str:
        """
        Given a query prompt, return a response
        """
