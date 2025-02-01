from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def save(self, file_path: str, data):
        """
        Save the given data into the concrete storage solution.
        The data is assumed to be in a JSON-serializable format (e.g. Python objects/lists)
        """
        pass
