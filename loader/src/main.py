import os

from dotenv import load_dotenv

from src.fs_access.local_fs_access.local_fs_access import LocalFSAccess
from src.loaders.sqlalchemy_loader.sqlalchemy_loader import SQLAlchemyLoader


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


def main():
    loader = SQLAlchemyLoader(get_pg_connection_uri())
    loader.load_json(LocalFSAccess(directory="./"))


if __name__ == "__main__":
    main()
