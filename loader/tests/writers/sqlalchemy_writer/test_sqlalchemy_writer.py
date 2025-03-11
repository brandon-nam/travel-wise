import datetime
from typing import Any
from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy.orm import Session

import src.writers.sqlalchemy_writer.sqlalchemy_writer as writer
from writers.sqlalchemy_writer.sqlalchemy_models import Post, Comment


@pytest.fixture
def mock_json_data() -> dict[str, Any]:
    return {
        "posts": [
            {
                "title": "Weekly Japan Travel Information and Discussion Thread - February 14, 2025",
                "id": "1ipa23o",
                "url": "https://www.reddit.com/r/JapanTravel/comments/1ipa23o/weekly_japan_travel_information_and_discussion/",
                "score": 3,
                "num_comments": 11,
                "country": "japan", 
            },
            {
                "title": "Itinerary check, plus is Ito worth it?",
                "id": "1iqp6jv",
                "url": "https://www.reddit.com/r/JapanTravel/comments/1iqp6jv/itinerary_check_plus_is_ito_worth_it/",
                "score": 2,
                "num_comments": 2,
                "country": "japan", 
            },
        ],
        "comments": [
            {
                "id": "mcx473k",
                "body": "I\u2019ll be in Tokyo Feb 27 - March 2 ahead of some work travel. I\u2019m hoping to see some snow and trying to figure out a good 1-2 night trip to do so. Yudanaka or Shibu onsen look promising, especially with the monkeys. I\u2019m curious about:\n\n1. Other good options to consider? Ideally within ~3 hours train, and a little more to do than *just* hang around the ryokan\n2. Any advice for finding ryokan that take solo travelers?",
                "score": 1,
                "post_id": "1ipa23o",
                "classification": "travel_suggestion",
                "characteristic": "accommodation and activities",
                "summary": "Ryokan for solo travellers, short term stay",
                "locations": [
                    {
                        "lat": 36.7446,
                        "lng": 138.4264,
                        "location_name": "Yudanaka",
                        "characteristic": "hot spring town",
                    },
                    {
                        "lat": 36.7399,
                        "lng": 138.4393,
                        "location_name": "Shibu Onsen",
                        "characteristic": "hot spring town",
                    },
                ],
                "start_date": datetime.date(2024, 2, 27),
                "end_date": datetime.date(2024, 3, 2),
            },
            {
                "id": "md20b1m",
                "body": 'Has anyone done the "**Mobile Suica APK**" thing to get around Android limitations for the Suica? Is it safe/working? Thanks',
                "score": 1,
                "post_id": "1ipa23o",
                "classification": "travel_tip",
                "characteristic": "tech solution",
                "summary": "Mobile Suica App on Android",
                "locations": [],
                "start_date": None,
                "end_date": None,
            },
        ],
    }


@pytest.fixture
def mock_writer(db_uri: str) -> writer.SQLAlchemyWriter:
    return writer.SQLAlchemyWriter(db_uri)


@pytest.fixture
def mock_engine() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_session() -> MagicMock:
    return MagicMock()


def test_create_session(
    db_uri: str,
    mock_engine: MagicMock,
    mock_session: MagicMock,
    mock_writer: writer.SQLAlchemyWriter,
) -> None:
    with (
        patch(
            "src.writers.sqlalchemy_writer.sqlalchemy_writer.create_engine"
        ) as mock_create_engine,
        patch(
            "src.writers.sqlalchemy_writer.sqlalchemy_writer.sessionmaker"
        ) as mock_session_maker,
        patch("src.writers.sqlalchemy_writer.sqlalchemy_writer.Base") as mock_base,
    ):
        mock_create_engine.return_value = mock_engine
        mock_session_maker.return_value = lambda: mock_session
        with mock_writer.create_session() as session:
            mock_create_engine.assert_called_once_with(db_uri)
            mock_session_maker.assert_called_once_with(bind=mock_engine)
            mock_base.metadata.create_all.assert_called_once_with(mock_engine)
            assert session == mock_session
            mock_session.commit.assert_not_called()

        mock_session.commit.assert_called_once()  # commit only called after session context exited
        mock_session.close.assert_called_once()  # check that session is closed at the end


def test_create_session_raises(
    db_uri: str, mock_session: MagicMock, mock_writer: writer.SQLAlchemyWriter
) -> None:
    with (
        patch("src.writers.sqlalchemy_writer.sqlalchemy_writer.Base") as mock_base,
        patch(
            "src.writers.sqlalchemy_writer.sqlalchemy_writer.sessionmaker"
        ) as mock_session_maker,
    ):
        mock_session_maker.return_value = lambda: mock_session
        mock_base.metadata.create_all.side_effect = Exception(
            "Database connection failed"
        )

        with pytest.raises(Exception, match="Database connection failed"):
            with mock_writer.create_session():
                pass
        mock_session.close.assert_called_once()


def test_write_json(
    mock_writer: writer.SQLAlchemyWriter,
    db_session: Session,
    mock_json_data: dict[str, Any],
) -> None:

    with patch(
        "src.writers.sqlalchemy_writer.sqlalchemy_writer.sessionmaker"
    ) as mock_session_maker:
        mock_session_maker.return_value = lambda: db_session

        mock_writer.write_json(mock_json_data)

        mock_posts = mock_json_data["posts"]
        mock_comments = mock_json_data["comments"]
        mock_locations = {
            (loc["lat"], loc["lng"], loc["location_name"], loc["characteristic"])
            for comment in mock_json_data["comments"]
            for loc in comment.get("locations", [])
        }
        posts = db_session.query(Post).all()
        comments = db_session.query(Comment).all()
        locations = set()

        for i, post in enumerate(posts):
            assert post.title == mock_posts[i]["title"]
            assert post.url == mock_posts[i]["url"]
            assert post.id == mock_posts[i]["id"]
            assert post.score == mock_posts[i]["score"]
            assert post.num_comments == mock_posts[i]["num_comments"]

        for i, comment in enumerate(comments):
            assert comment.id == mock_comments[i]["id"]
            assert comment.body == mock_comments[i]["body"]
            assert comment.score == mock_comments[i]["score"]
            assert comment.post_id == mock_comments[i]["post_id"]
            assert comment.classification.value == mock_comments[i]["classification"]
            assert comment.start_date == mock_comments[i]["start_date"]
            assert comment.end_date == mock_comments[i]["end_date"]
            assert comment.summary == mock_comments[i]["summary"]
            for location in comment.locations:
                locations.add(
                    (
                        location.lat,
                        location.lng,
                        location.location_name,
                        location.characteristic,
                    )
                )
        assert locations == mock_locations
