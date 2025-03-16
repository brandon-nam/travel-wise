from src.handlers.base_handler import BaseHandler
from src.handlers.reddit.post.add_countries_handler import AddCountriesHandler
from src.transformers.reddit.reddit_transformer import RedditTransformer

HANDLERS = [AddCountriesHandler()]


class RedditPostTransformer(RedditTransformer):
    @property
    def chain(self) -> list[BaseHandler]:
        return HANDLERS

    @property
    def prefix(self) -> str:
        return "posts_"
