import logging
from contextlib import contextmanager

from constants.reddit import ClassificationType
from database.sqlalchemy.models import Base, Post, Comment, Location
from database.sqlalchemy.repository import Repository
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from src.writers.base_writer import BaseWriter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


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

    def write_posts(self, json_data: list[dict]) -> None:
        with self.create_session() as session:
            repo = Repository(session)
            for post in json_data:
                try:
                    repo.add(
                        Post,
                        id=post["id"],
                        title=post["title"],
                        url=post["url"],
                        score=post["score"],
                        num_comments=post["num_comments"],
                        country=post["country"],
                    )
                except IntegrityError as e:
                    logger.info(
                        f"IntegrityError {e}, ignoring post with id={post['id']}"
                    )

    def write_comments(self, json_data: list[dict]) -> None:
        with self.create_session() as session:
            repo = Repository(session)
            for comment in json_data:
                try:
                    repo.add(
                        Comment,
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
                except IntegrityError as e:
                    logger.info(
                        f"IntegrityError {e}, ignoring comment with id={comment['id']}"
                    )

            for comment in json_data:
                for loc in comment["locations"]:
                    try:
                        repo.add(
                            Location,
                            comment_id=comment["id"],
                            lat=loc["lat"],
                            lng=loc["lng"],
                            location_name=loc["location_name"],
                            characteristic=loc["characteristic"],
                        )
                    except IntegrityError as e:
                        logger.info(
                            f"IntegrityError {e}, ignoring location ({loc['lat']}, {loc['lng']})with id={comment['id']}"
                        )
