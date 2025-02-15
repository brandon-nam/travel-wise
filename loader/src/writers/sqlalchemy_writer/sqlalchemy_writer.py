from contextlib import contextmanager
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.writers.base_writer import BaseWriter
from src.writers.sqlalchemy_writer.sqlalchemy_models import (
    Base,
    Post,
    Comment,
    ClassificationType,
    Location,
)


class SQLAlchemyWriter(BaseWriter):
    def __init__(self, db_uri: str):
        self.db_uri = db_uri

    @contextmanager
    def create_session(self) -> Session:
        engine = create_engine(self.db_uri)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        try:
            yield session
        finally:
            session.close()

    def write_json(self, json_data: dict[str, Any]) -> None:
        post_data = json_data["posts"]
        comment_data = json_data["comments"]
        posts = [
            Post(
                id=post["id"],
                title=post["title"],
                url=post["url"],
                karma=post["karma"],
                num_comments=post["num_comments"],
            )
            for post in post_data
        ]
        comments = [
            Comment(
                id=comment["id"],
                post_id=comment["post_id"],
                body=comment["body"],
                karma=comment["karma"],
                classification=ClassificationType[comment["classification"]],
                start_date=comment["start_date"],
                end_date=comment["end_date"],
            )
            for comment in comment_data
        ]
        locations = [
            Location(comment_id=comment["id"], lat=loc["lat"], lng=loc["lng"])
            for comment in comment_data
            for loc in comment["locations"]
        ]

        with self.create_session() as session:
            for row_list in (posts, comments, locations):
                session.add_all(row_list)
                session.commit()
