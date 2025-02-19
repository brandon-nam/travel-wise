import json

from ai_provider.openai_provider.open_ai_provider import OpenAIProvider
from fs_access.base_fs_access import BaseFSAccess
from handlers.reddit.classify_location_coordinates_handler import (
    ClassifyLocationCoordinatesHandler,
)
from handlers.reddit.classify_suggestion_or_tip_handler import (
    ClassifySuggestionOrTipHandler,
)
from handlers.reddit.classify_temporal_handler import ClassifyTemporalHandler
from handlers.reddit.split_posts_and_comments_handler import (
    SplitPostsAndCommentsHandler,
)
from transformers.base_transformer import BaseTransformer


class RedditTransformer(BaseTransformer):
    def __init__(self, fs_access: BaseFSAccess):
        openai_provider = OpenAIProvider()
        self._chain = [
            SplitPostsAndCommentsHandler(),
            ClassifySuggestionOrTipHandler(openai_provider),
            ClassifyLocationCoordinatesHandler(openai_provider),
            ClassifyTemporalHandler(openai_provider),
        ]
        super().__init__(fs_access)

    @property
    def chain(self) -> list:
        return self._chain

    def transform(self) -> None:
        for file_path in self.fs_access.get_src_file_paths("json"):
            with self.fs_access.open(file_path) as f:
                json_data = json.load(f)

            transformed_file_path = self.fs_access.get_transformed_file_path(file_path)

            with self.fs_access.open(transformed_file_path, "w") as f:
                str_result = self.chain[0].handle(json.dumps(json_data))
                json_result = json.loads(str_result)
                json.dump(json_result, f, indent=4)
