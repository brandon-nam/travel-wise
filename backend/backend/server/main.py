from flask import Flask

from backend.server.routes import create_routes


def create_app() -> Flask:
    app = Flask(__name__)
    return app


def main() -> None:
    app = create_app()
    create_routes(app)
    app.run(host="0.0.0.0", port=3203)


if __name__ == "__main__":
    main()
