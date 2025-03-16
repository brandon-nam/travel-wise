from src.handlers.base_handler import BaseHandler
from src.handlers.reddit.comment.classify_location_coordinates_handler import (
    ClassifyLocationCoordinatesHandler,
)
from src.handlers.reddit.comment.classify_suggestion_or_tip_handler import (
    ClassifySuggestionOrTipHandler,
)
from src.handlers.reddit.comment.classify_temporal_handler import (
    ClassifyTemporalHandler,
)
from src.handlers.reddit.comment.location_deduplication_handler import (
    LocationDeduplicationHandler,
)
from src.handlers.reddit.comment.cleanup_comments_handler import CleanupCommentsHandler


from src.handlers.reddit.comment.summarise_posts_handler import SummarisePostsHandler
from src.transformers.reddit.reddit_transformer import RedditTransformer

HANDLERS = [
    CleanupCommentsHandler(),
    ClassifySuggestionOrTipHandler(RedditTransformer.openai_provider),
    ClassifyLocationCoordinatesHandler(RedditTransformer.openai_provider),
    LocationDeduplicationHandler(),
    ClassifyTemporalHandler(RedditTransformer.openai_provider),
    SummarisePostsHandler(RedditTransformer.openai_provider),
]


class RedditCommentTransformer(RedditTransformer):
    @property
    def chain(self) -> list[BaseHandler]:
        return HANDLERS

    @property
    def prefix(self) -> str:
        return "comments_"
