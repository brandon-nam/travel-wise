from flask import Response, Flask

from src.database.base import BaseDB


def create_routes(app: Flask, database: BaseDB) -> None:
    @app.route("/posts", methods=["GET"])
    def get_posts() -> Response:
        return database.get_posts()

    @app.route("/comments", methods=["GET"])
    def get_comments() -> Response:
        return database.get_comments()
