import json
from abc import ABC, abstractmethod

from src.writers.base_writer import BaseWriter


class Loader(ABC):
    @abstractmethod
    def create_writer(self) -> BaseWriter:
        pass

    def load(self):
        writer = self.create_writer()

        with open("./dummy_japan.json") as f:
            json_data = json.load(f)

        writer.write_json(json_data)
