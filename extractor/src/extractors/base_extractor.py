from abc import ABC


class BaseExtractor(ABC):
    def extract(self) -> None:
        pass
