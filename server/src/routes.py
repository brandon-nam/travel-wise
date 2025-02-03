from flask import Flask, request, jsonify


def create_routes(app: Flask) -> None:
    @app.route("/")
    def home():
        return "Welcome to TravelWise"

    @app.route("/query", methods=["POST"])
    def query() -> str:
        return jsonify(request.json)
