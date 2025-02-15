from src.loaders.loader import Loader
from src.writers.base_writer import BaseWriter
from src.writers.sqlalchemy_writer.sqlalchemy_writer import SQLAlchemyWriter


class SQLAlchemyLoader(Loader):
    def __init__(self, db_uri: str):
        self.db_uri = db_uri

    def create_writer(self) -> BaseWriter:
        return SQLAlchemyWriter(self.db_uri)
