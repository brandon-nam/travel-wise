from flask import Response, Flask, request

from src.repository.server_repository import ServerRepository


def create_routes(app: Flask, repo: ServerRepository) -> None:
    @app.route("/posts", methods=["GET"])
    def get_posts() -> Response:
        return repo.get_posts()

    @app.route("/comments", methods=["GET"])
    def get_comments() -> Response:
        classification = request.args.get("classification")
        country = request.args.get("country")
        return repo.get_comments(classification=classification, country=country)

    @app.route("/countries", methods=["GET"])
    def get_countries() -> Response:
        return repo.get_countries()
