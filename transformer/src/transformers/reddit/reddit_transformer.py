import json
import logging
import os

from fs_access.base_fs_access import BaseFSAccess

from src.ai_provider.openai_provider.open_ai_provider import OpenAIProvider
from src.handlers.base_handler import BaseHandler


from src.transformers.base_transformer import BaseTransformer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


class RedditTransformer(BaseTransformer):
    openai_provider = OpenAIProvider()

    def __init__(self, fs_access: BaseFSAccess):
        super().__init__(fs_access)

    @property
    def chain(self) -> list[BaseHandler]:
        raise NotImplementedError()

    @property
    def prefix(self) -> str:
        raise NotImplementedError()

    def transform(self) -> None:
        src_directory = "raw_data"
        target_directory = "transformed_data"

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        for file_path in self.fs_access.get_file_paths(
            directory=src_directory, file_type="json"
        ):
            if self.prefix not in file_path:
                continue
            logger.info(f"Transforming {file_path}...")
            with self.fs_access.open(file_path) as f:
                json_data = json.load(f)
            transformed_file_path = os.path.join(
                target_directory, os.path.basename(file_path)
            )

            if os.path.exists(transformed_file_path):
                logger.info(f"file {transformed_file_path} already exists, skipping...")
                continue

            with self.fs_access.open(transformed_file_path, "w") as f:
                str_result = self.chain[0].handle(json.dumps(json_data))
                json_result = json.loads(str_result)
                json.dump(json_result, f, indent=4)
            logger.info(f"Successfully transformed {file_path}!!!")
