import datetime
from typing import Any

import pytest
from flask_sqlalchemy.session import Session

from src.database.sqlalchemy_db.sqlalchemy_db import SQLAlchemyDB
from src.database.sqlalchemy_db.sqlalchemy_models import (
    Post,
    Comment,
    Location,
    db,
    ClassificationType,
)


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
    model_class: db.Model, rows: list[dict[str, Any]], db_session: Session
) -> None:
    for row in rows:
        db_session.add(model_class(**row))
    db_session.commit()


def test_get_posts(sqlalchemy_db: SQLAlchemyDB, db_session: Session) -> None:
    posts = [
        {
            "id": "1ijug04",
            "title": "Weekly Japan Travel Information and Discussion Thread - February 07, 2025",
            "url": "https://www.reddit.com/r/JapanTravel/comments/1ijug04/weekly_japan_travel_information_and_discussion/",
            "score": 12,
            "num_comments": 7,
            "country": "Japan",
        },
        {
            "id": "2ijug05",
            "title": "Japan Travel Tips and Recommendations",
            "url": "https://www.reddit.com/r/JapanTravel/comments/2ijug05/japan_travel_tips_and_recommendations/",
            "score": 15,
            "num_comments": 10,
            "country": "Japan",
        },
    ]
    add_rows_to_table(Post, posts, db_session)

    response = sqlalchemy_db.get_posts()

    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 2
    for i, post in enumerate(posts):
        for k, v in post.items():
            assert data[i][k] == v


def test_get_comments_returns_all_comments(
    sqlalchemy_db: SQLAlchemyDB,
    db_session: Session,
    mock_locations: list[dict[str, Any]],
    mock_comments: list[dict[str, Any]],
    add_rows_to_db,
) -> None:

    response = sqlalchemy_db.get_comments()

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == len(mock_comments)

    for i, comment in enumerate(mock_comments):
        comment_response = data[i]
        comment_response["classification"] = ClassificationType(
            comment_response["classification"]
        )
        comment_response["start_date"] = datetime.datetime.strptime(
            comment_response["start_date"], "%a, %d %b %Y %H:%M:%S %Z"
        ).date()
        comment_response["end_date"] = datetime.datetime.strptime(
            comment_response["end_date"], "%a, %d %b %Y %H:%M:%S %Z"
        ).date()
        for k, v in comment.items():
            assert comment_response[k] == v
        print(comment_response["location_coordinates"])

        assert len(comment_response["location_coordinates"]) == 1
        location_response = comment_response["location_coordinates"][0]
        for coordinate_type in ("lat", "lng"):
            assert (
                location_response[coordinate_type] == mock_locations[i][coordinate_type]
            )


@pytest.mark.parametrize(
    "classification, expected_count",
    [("", 5), ("travel-tip", 2), ("travel-suggestion", 2), ("other", 1), ("blabla", 5)],
)
def test_get_comments_classification_filter(
    sqlalchemy_db: SQLAlchemyDB,
    classification: str,
    expected_count: int,
    add_rows_to_db,
) -> None:
    response = sqlalchemy_db.get_comments(classification=classification, country="")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == expected_count


@pytest.mark.parametrize(
    "country, expected_count",
    [("japan", 3), ("korea", 2)],
)
def test_get_comments_country_filter(
    sqlalchemy_db: SQLAlchemyDB,
    country: str,
    expected_count: int,
    add_rows_to_db,
) -> None:
    response = sqlalchemy_db.get_comments(classification="", country=country)

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == expected_count
