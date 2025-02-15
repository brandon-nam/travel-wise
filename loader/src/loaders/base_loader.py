import json
import logging
from abc import ABC, abstractmethod


from src.fs_access.base_fs_access import BaseFSAccess
from src.writers.base_writer import BaseWriter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Loader(ABC):
    """
    Abstract loader factory.
    Call self.create_writer() to get the concrete writer object.
    """

    @abstractmethod
    def create_writer(self) -> BaseWriter:
        pass

    def load_json(self, fs_access: BaseFSAccess):
        """
        Write content from a JSON file into the database.
        fs_access should be a subclass of BaseFSAccess.
        """
        writer = self.create_writer()
        for file_path in fs_access.get_file_paths(file_type="json"):
            logger.info(f"{file_path}: attempting to load...")
            with fs_access.open(file_path) as f:
                json_data = json.load(f)
            try:
                writer.write_json(json_data)
            except Exception as e:
                logger.info(f"{file_path}: failed to load due to: {e.orig}")
            else:
                logger.info(f"{file_path} successfully loaded file")
