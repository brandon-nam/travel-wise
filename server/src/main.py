import os
from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS

from src.database.base_db import BaseDB
from src.database.sqlalchemy_db.sqlalchemy_db import SQLAlchemyDB
from src.routes.routes import create_routes

load_dotenv()


def get_pg_connection_uri() -> str:
    db_host, db_port, db_user, db_password, db_name = (
        os.getenv("DB_HOST") or "localhost",
        os.getenv("DB_PORT") or "5432",
        os.getenv("DB_USER") or "postgres",
        os.getenv("DB_PASSWORD") or "",
        os.getenv("DB_NAME") or "travelwise",
    )
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_app(database: BaseDB) -> Flask:
    app = Flask(__name__)
    CORS(app)
    database.setup_db(app)
    create_routes(app, database)
    return app


def main() -> None:
    app = create_app(SQLAlchemyDB(get_pg_connection_uri()))
    app.run(host="0.0.0.0", port=3203)


if __name__ == "__main__":
    main()
