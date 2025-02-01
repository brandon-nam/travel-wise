import json

from storage.storage import Storage


class LocalStorage(Storage):
    def save(self, file_path: str, data) -> None:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
