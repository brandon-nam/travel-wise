from flask import Response, Flask, request

from src.database.base_db import BaseDB


def create_routes(app: Flask, database: BaseDB) -> None:
    @app.route("/posts", methods=["GET"])
    def get_posts() -> Response:
        return database.get_posts()

    @app.route("/comments", methods=["GET"])
    def get_comments() -> Response:
        classification = request.args.get("classification")
        country = request.args.get("country")
        return database.get_comments(classification=classification, country=country)
