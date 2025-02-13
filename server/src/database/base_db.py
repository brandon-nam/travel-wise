from abc import ABC, abstractmethod

from flask import Response, Flask


class BaseDB(ABC):
    def __init__(self, db_connection_uri: str) -> None:
        self.db_connection_uri = db_connection_uri

    @abstractmethod
    def setup_db(self, app: Flask) -> None:
        """
        connect your app to the database
        """
        pass

    @abstractmethod
    def get_posts(self) -> Response:
        pass

    @abstractmethod
    def get_comments(self) -> Response:
        pass
