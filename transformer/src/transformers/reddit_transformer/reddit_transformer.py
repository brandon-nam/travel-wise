import json
import os

from fs_access.base_fs_access import BaseFSAccess

from src.ai_provider.openai_provider.open_ai_provider import OpenAIProvider
from src.handlers.base_handler import BaseHandler
from src.handlers.reddit.classify_location_coordinates_handler import (
    ClassifyLocationCoordinatesHandler,
)
from src.handlers.reddit.classify_suggestion_or_tip_handler import (
    ClassifySuggestionOrTipHandler,
)
from src.handlers.reddit.classify_temporal_handler import ClassifyTemporalHandler
from src.handlers.reddit.location_deduplication_handler import (
    LocationDeduplicationHandler,
)
from src.handlers.reddit.cleanup_comments_handler import CleanupCommentsHandler
from src.handlers.reddit.split_posts_and_comments_handler import (
    SplitPostsAndCommentsHandler,
)

from src.handlers.reddit.add_countries_handler import (
    AddCountriesHandler,
)

from src.handlers.reddit.summarise_posts_handler import SummarisePostsHandler
from src.transformers.base_transformer import BaseTransformer


class RedditTransformer(BaseTransformer):
    def __init__(self, fs_access: BaseFSAccess):
        openai_provider = OpenAIProvider()
        self._chain = [
            SplitPostsAndCommentsHandler(),
            CleanupCommentsHandler(),
            ClassifySuggestionOrTipHandler(openai_provider),
            ClassifyLocationCoordinatesHandler(openai_provider),
            LocationDeduplicationHandler(),
            ClassifyTemporalHandler(openai_provider),
            SummarisePostsHandler(openai_provider),
            AddCountriesHandler(),
        ]
        super().__init__(fs_access)

    @property
    def chain(self) -> list[BaseHandler]:
        return self._chain

    def transform(self) -> None:
        src_directory = "raw_data"
        target_directory = "transformed_data"

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        for file_path in self.fs_access.get_file_paths(
            directory=src_directory, file_type="json"
        ):
            with self.fs_access.open(file_path) as f:
                json_data = json.load(f)

            transformed_file_path = os.path.join(
                target_directory, os.path.basename(file_path)
            )

            with self.fs_access.open(transformed_file_path, "w") as f:
                str_result = self.chain[0].handle(json.dumps(json_data))
                json_result = json.loads(str_result)
                json.dump(json_result, f, indent=4)
