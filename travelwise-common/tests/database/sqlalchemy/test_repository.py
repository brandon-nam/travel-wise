import datetime
from typing import Any
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from constants.reddit import ClassificationType
from database.sqlalchemy.models import Post, Comment, Location
from database.sqlalchemy.repository import Repository


@pytest.fixture
def mock_data(
    mock_posts: list[dict[str, Any]],
    mock_comments: list[dict[str, Any]],
    mock_locations: list[dict[str, Any]],
) -> dict:
    return {
        Post: mock_posts,
        Comment: mock_comments,
        Location: mock_locations,
    }


@pytest.fixture
def mock_posts() -> list[dict[str, Any]]:
    return [
        {
            "id": "1ijug04",
            "title": "Weekly Japan Travel Information and Discussion Thread - February 07, 2025",
            "url": "https://www.reddit.com/r/JapanTravel/comments/1ijug04/weekly_japan_travel_information_and_discussion/",
            "score": 12,
            "num_comments": 7,
            "country": "japan",
        },
        {
            "id": "1ijug05",
            "title": "Weekly Korea Travel Information and Discussion Thread - February 07, 2025",
            "url": "https://www.reddit.com/r/KoreaTravel/comments/1ijug04/weekly_korea_travel_information_and_discussion/",
            "score": 12,
            "num_comments": 7,
            "country": "korea",
        },
    ]


@pytest.fixture
def mock_comments() -> list[dict[str, Any]]:
    return [
        {
            "id": "mbomop8",
            "post_id": "1ijug04",
            "body": "Traveling to Kamakura from Tokyo next week. Can anyone recommend the best way to get to Yokohama chinatown on my way back to Tokyo? I did this last year and the taxi ride seemed too long from whatever station in Yokohama I arrived in from Kamakura which google maps recommended.",
            "score": 1,
            "classification": ClassificationType.travel_suggestion,
            "start_date": datetime.date(2025, 2, 1),
            "end_date": datetime.date(2025, 2, 7),
            "characteristic": "transport",
            "summary": "Best way to get to Yokohama in between Kamakura and Tokyo",
        },
        {
            "id": "mbr1lyf",
            "post_id": "1ijug04",
            "body": "I recommend you try this and do that (random tip).",
            "score": 1,
            "classification": ClassificationType.travel_tip,
            "start_date": datetime.date(2025, 2, 1),
            "end_date": datetime.date(2025, 2, 7),
            "characteristic": "itinerary",
            "summary": "Random japan tip",
        },
        {
            "id": "m123456",
            "post_id": "1ijug04",
            "body": "random comment",
            "score": 1,
            "classification": ClassificationType.other,
            "start_date": datetime.date(2025, 2, 1),
            "end_date": datetime.date(2025, 2, 7),
            "characteristic": "random",
            "summary": "random comment",
        },
        {
            "id": "m123457",
            "post_id": "1ijug05",
            "body": "random comment",
            "score": 2,
            "classification": ClassificationType.travel_suggestion,
            "start_date": datetime.date(2025, 2, 1),
            "end_date": datetime.date(2025, 2, 7),
            "characteristic": "random",
            "summary": "random comment",
        },
        {
            "id": "m123458",
            "post_id": "1ijug05",
            "body": "random comment",
            "score": 3,
            "classification": ClassificationType.travel_tip,
            "start_date": datetime.date(2025, 2, 1),
            "end_date": datetime.date(2025, 2, 7),
            "characteristic": "random",
            "summary": "random comment",
        },
    ]


@pytest.fixture
def mock_locations() -> list[dict[str, Any]]:
    return [
        {
            "id": "loc1",
            "lat": 35.3195,
            "lng": 139.5502,
            "comment_id": "mbomop8",
            "location_name": "Tokyo",
            "characteristic": "City",
        },
        {
            "id": "loc2",
            "lat": 35.3215,
            "lng": 139.5510,
            "comment_id": "mbr1lyf",
            "location_name": "Disneyland",
            "characteristic": "Theme Park",
        },
        {
            "id": "loc3",
            "lat": 34.1111,
            "lng": 123.4567,
            "comment_id": "m123456",
            "location_name": "Maihama",
            "characteristic": "Neighbourhood",
        },
        {
            "id": "loc4",
            "lat": 32.111,
            "lng": 123.4567,
            "comment_id": "m123457",
            "location_name": "Somewhere",
            "characteristic": "on earth",
        },
        {
            "id": "loc5",
            "lat": 43.222,
            "lng": 123.4567,
            "comment_id": "m123458",
            "location_name": "nowhere",
            "characteristic": "on earth",
        },
    ]


@pytest.fixture
def add_rows_to_db(
    mock_posts: list[dict[str, Any]],
    mock_comments: list[dict[str, Any]],
    mock_locations: list[dict[str, Any]],
    db_session: Session,
) -> None:
    add_rows_to_table(Post, mock_posts, db_session)
    add_rows_to_table(Comment, mock_comments, db_session)
    add_rows_to_table(Location, mock_locations, db_session)


def add_rows_to_table(
    model_class: Post.__class__ | Comment.__class__ | Location.__class__,
    rows: list[dict[str, Any]],
    db_session: Session,
) -> None:
    for row in rows:
        db_session.add(model_class(**row))
    db_session.commit()


@pytest.fixture
def repository(db_session: Session) -> Repository:
    return Repository(db_session)


@pytest.mark.parametrize("model_class", (Post, Comment, Location))
def test_get_all(
    add_rows_to_db, model_class, repository: Repository, mock_data: dict
) -> None:
    posts = repository.get_all(model_class)
    mock_data_list = mock_data.get(model_class)

    assert len(posts) == len(mock_data_list)

    for i, data in enumerate(posts):
        mock_data = mock_data_list[i]
        for k, v in mock_data.items():
            assert getattr(data, k) == v


def test_filter(
    add_rows_to_db,
    repository: Repository,
) -> None:
    country = "japan"
    result = repository.filter(Post, country=country)
    assert len(result) == 1
    assert result[0].country == country


def test_get(
    add_rows_to_db,
    repository: Repository,
) -> None:
    post = repository.get(Post, "1ijug04")
    assert post is not None
    assert post.id == "1ijug04"


def test_commit_rollback(
    repository: Repository,
) -> None:
    mock_session = MagicMock()
    repository.session = mock_session
    repository.commit()
    mock_session.commit.assert_called_once()
    repository.rollback()
    mock_session.rollback.assert_called_once()


@pytest.mark.parametrize("model_class", (Post, Comment, Location))
def test_add(
    model_class: Post.__class__ | Comment.__class__ | Location.__class__,
    repository: Repository,
    db_session: Session,
    mock_data: dict,
) -> None:
    mock_data_list = mock_data.get(model_class)
    for row in mock_data_list:
        repository.add(model_class, **row)
    assert len(repository.get_all(model_class)) == len(mock_data_list)


def test_update(
    add_rows_to_db,
    repository: Repository,
    db_session: Session,
) -> None:
    updated_data = {
        "title": "Updated Title",
        "score": 10,
    }

    repository.update(Post, "1ijug04", **updated_data)
    db_post = db_session.get(Post, "1ijug04")
    assert db_post.title == "Updated Title"
    assert db_post.score == updated_data["score"]


def test_delete(
    add_rows_to_db,
    repository: Repository,
    db_session: Session,
) -> None:
    deleted = repository.delete(Post, "1ijug04")
    assert deleted
    db_post = db_session.get(Post, "1ijug04")
    assert db_post is None
