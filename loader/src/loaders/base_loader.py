import json
import logging
from abc import ABC, abstractmethod
from typing import Callable

from fs_access.base_fs_access import BaseFSAccess

from src.writers.base_writer import BaseWriter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BaseLoader(ABC):
    """
    Abstract loader factory.
    Call self.create_writer() to get the concrete writer object.
    """

    @abstractmethod
    def create_writer(self) -> BaseWriter:
        pass

    def write(
        self, fs_access: BaseFSAccess, file_path: str, write_method: Callable
    ) -> None:
        with fs_access.open(file_path) as f:
            json_data = json.load(f)
        try:
            write_method(json_data)
        except Exception as e:
            logger.info(f"{file_path}: failed to load due to: {e}")
        else:
            logger.info(f"{file_path} successfully loaded file")

    def load_json(self, fs_access: BaseFSAccess):
        """
        Write content from a JSON file into the database.
        fs_access should be a subclass of BaseFSAccess.
        """
        writer = self.create_writer()
        posts_file_paths = []
        comments_file_paths = []

        for file_path in fs_access.get_file_paths(directory="", file_type="json"):
            if file_path.startswith("posts_"):
                posts_file_paths.append(file_path)

            if file_path.startswith("comments_"):
                comments_file_paths.append(file_path)
        for file_path in posts_file_paths:
            self.write(fs_access, file_path, writer.write_posts)

        for file_path in comments_file_paths:
            self.write(fs_access, file_path, writer.write_comments)
