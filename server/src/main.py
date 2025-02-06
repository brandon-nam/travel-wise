import os

from flask import Flask
from flask_cors import CORS

from src.database.sqlalchemy_db import SQLAlchemyDB
from src.routes.routes import create_routes


def get_pg_connection_uri() -> str:
    db_host, db_port, db_user, db_password, db_name = (
        os.getenv("DB_HOST") or "localhost",
        os.getenv("DB_PORT") or "5432",
        os.getenv("DB_USER") or "postgres",
        os.getenv("DB_PASSWORD") or "",
        os.getenv("DB_NAME") or "travelwise",
    )
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    database = SQLAlchemyDB(app, get_pg_connection_uri())
    database.setup_db()
    create_routes(app, database)
    return app


def main() -> None:
    app = create_app()
    app.run(host="0.0.0.0", port=3203)


if __name__ == "__main__":
    main()
