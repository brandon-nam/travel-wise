import datetime
from typing import Any

from flask_sqlalchemy.session import Session

from src.database.sqlalchemy_db.sqlalchemy_db import SQLAlchemyDB
from src.database.sqlalchemy_db.sqlalchemy_models import (
    Post,
    Comment,
    Location,
    db,
    ClassificationType,
)


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
        },
        {
            "id": "2ijug05",
            "title": "Japan Travel Tips and Recommendations",
            "url": "https://www.reddit.com/r/JapanTravel/comments/2ijug05/japan_travel_tips_and_recommendations/",
            "score": 15,
            "num_comments": 10,
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


def test_get_comments(sqlalchemy_db: SQLAlchemyDB, db_session: Session) -> None:
    posts = [
        {
            "id": "1ijug04",
            "title": "Weekly Japan Travel Information and Discussion Thread - February 07, 2025",
            "url": "https://www.reddit.com/r/JapanTravel/comments/1ijug04/weekly_japan_travel_information_and_discussion/",
            "score": 12,
            "num_comments": 7,
        }
    ]
    comments = [
        {
            "id": "mbomop8",
            "post_id": "1ijug04",
            "body": "Traveling to Kamakura from Tokyo next week. Can anyone recommend the best way to get to Yokohama chinatown on my way back to Tokyo? I did this last year and the taxi ride seemed too long from whatever station in Yokohama I arrived in from Kamakura which google maps recommended.",
            "score": 1,
            "classification": ClassificationType.travel_suggestion,
            "start_date": datetime.date(2025, 2, 1),
            "end_date": datetime.date(2025, 2, 7),
        },
        {
            "id": "mbr1lyf",
            "post_id": "1ijug04",
            "body": "Heading to Japan in May, I''ve got a rough idea of what I am doing but need some help with accommodation recommendations, I''m going solo so I don''t need a lot but I don''t want to stay at hostels or capsule places...",
            "score": 1,
            "classification": ClassificationType.travel_suggestion,
            "start_date": datetime.date(2025, 2, 1),
            "end_date": datetime.date(2025, 2, 7),
        },
    ]
    locations = [
        {"id": "loc1", "lat": 35.3195, "lng": 139.5502, "comment_id": "mbomop8"},
        {"id": "loc2", "lat": 35.3215, "lng": 139.5510, "comment_id": "mbr1lyf"},
    ]

    add_rows_to_table(Post, posts, db_session)
    add_rows_to_table(Comment, comments, db_session)
    add_rows_to_table(Location, locations, db_session)

    response = sqlalchemy_db.get_comments()

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == len(comments)

    for i, comment in enumerate(comments):
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

        assert len(comment_response["location_coordinates"]) == 1
        location_response = comment_response["location_coordinates"][0]
        for coordinate_type in ("lat", "lng"):
            assert location_response[coordinate_type] == locations[i][coordinate_type]
