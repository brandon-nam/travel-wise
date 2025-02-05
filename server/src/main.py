import os

from flask import Flask
from flask_cors import CORS
from flask.cli import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from models import db
from src.routes import create_routes


def setup_db(app: Flask, database: SQLAlchemy) -> None:
    load_dotenv()
    db_host, db_port, db_user, db_password, db_name = (
        os.getenv("DB_HOST") or "localhost",
        os.getenv("DB_PORT") or "5432",
        os.getenv("DB_USER") or "postgres",
        os.getenv("DB_PASSWORD") or "",
        os.getenv("DB_NAME") or "travelwise",
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    database.init_app(app)


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    setup_db(app, db)
    create_routes(app)
    return app


def main() -> None:
    app = create_app()
    app.run(host="0.0.0.0", port=3203)


if __name__ == "__main__":
    main()
