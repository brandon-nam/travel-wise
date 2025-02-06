from abc import ABC, abstractmethod

from flask import Flask, Response


class BaseDB(ABC):
    def __init__(self, app: Flask, db_connection_uri: str) -> None:
        self.app = app
        self.db_connection_uri = db_connection_uri

    @abstractmethod
    def setup_db(self) -> None:
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
