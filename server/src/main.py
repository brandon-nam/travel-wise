from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS

from src.repository.server_repository import ServerRepository
from src.routes.routes import create_routes

load_dotenv()


def create_app() -> Flask:
    repo = ServerRepository()
    app = Flask(__name__)
    CORS(app)
    repo.setup_db(app)
    create_routes(app, repo)
    return app


def main() -> None:
    app = create_app()
    app.run(host="0.0.0.0", port=3203)


if __name__ == "__main__":
    main()
