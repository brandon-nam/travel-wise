from flask import Flask

from src.routes import create_routes


def create_app() -> Flask:
    app = Flask(__name__)
    create_routes(app)
    return app


def main() -> None:
    app = create_app()
    app.run(host="0.0.0.0", port=3203)


if __name__ == "__main__":
    main()
