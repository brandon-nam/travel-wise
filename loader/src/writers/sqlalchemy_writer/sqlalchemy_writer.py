from contextlib import contextmanager
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
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
        """
        Handles opening and closing of session (context manager: with-clause to be used)
        If any error occurs, session is rolled back (no-op)
        """
        engine = create_engine(self.db_uri)
        session = sessionmaker(bind=engine)()
        try:
            Base.metadata.create_all(engine)
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def write_json(self, json_data: dict[str, Any]) -> None:
        # 3 sessions required because we need to insert Posts, Comments and Locations strictly in that order
        with self.create_session() as session:
            session.add_all(
                [
                    Post(
                        id=post["id"],
                        title=post["title"],
                        url=post["url"],
                        score=post["score"],
                        num_comments=post["num_comments"],
                        country=post["country"],
                    )
                    for post in json_data["posts"]
                ]
            )

        with self.create_session() as session:
            session.add_all(
                Comment(
                    id=comment["id"],
                    post_id=comment["post_id"],
                    body=comment["body"],
                    score=comment["score"],
                    classification=ClassificationType[comment["classification"]],
                    start_date=comment["start_date"],
                    end_date=comment["end_date"],
                    characteristic=comment["characteristic"],
                    summary=comment["summary"],
                )
                for comment in json_data["comments"]
            )

        with self.create_session() as session:
            session.add_all(
                [
                    Location(
                        comment_id=comment["id"],
                        lat=loc["lat"],
                        lng=loc["lng"],
                        location_name=loc["location_name"],
                        characteristic=loc["characteristic"],
                    )
                    for comment in json_data["comments"]
                    for loc in comment["locations"]
                ]
            )
