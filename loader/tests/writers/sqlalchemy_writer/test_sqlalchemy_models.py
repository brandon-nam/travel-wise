import datetime
from typing import Any

import pytest
from sqlalchemy.orm import Session

from writers.sqlalchemy_writer.sqlalchemy_models import (
    ClassificationType,
    Post,
    Comment,
    Location,
    Base,
)


@pytest.mark.parametrize(
    "enum_member, expected_value",
    [
        (ClassificationType.travel_tip, "travel_tip"),
        (ClassificationType.travel_suggestion, "travel_suggestion"),
        (ClassificationType.other, "other"),
    ],
)
def test_classification_type_enum(enum_member, expected_value):
    assert enum_member.value == expected_value


@pytest.mark.parametrize(
    "model_class, row_dict",
    [
        (
            Post,
            {
                "id": "1ijug04",
                "title": "Weekly Japan Travel Information and Discussion Thread - February 07, 2025",
                "url": "https://www.reddit.com/r/JapanTravel/comments/1ijug04/weekly_japan_travel_information_and_discussion/",
                "score": 12,
                "num_comments": 7,
            },
        ),
        (
            Comment,
            {
                "id": "mbp0pvu",
                "post_id": "1ijug04",
                "body": "In Japan quality is expected and generally delivered. In Tokyo alone there are 137,000 restaurants overall...",
                "score": 1,
                "classification": ClassificationType.travel_suggestion,
                "characteristic": "Food",
                "summary": "Restaurant quality in Japan",
                "start_date": datetime.date(2025, 2, 1),
                "end_date": datetime.date(2025, 2, 7),
            },
        ),
        (
            Location,
            {
                "id": "mbomop8",
                "lat": 35.3195,
                "lng": 139.5502,
                "location_name": "Tokyo",
                "characteristic": "City",
            },
        ),
    ],
)
def test_create_model(
    model_class: Base, row_dict: dict[str, Any], db_session: Session
) -> None:
    """
    Test to ensure that created models are accurate. If a new model is added to sqlalchemy_models.py,
    please test it here.

    :param model_class: Class type which extends db.Model
    :param row_dict: A mapping containing for a single row's columns -> values
    :param db_session: Session defined in conftest.py
    :return: None
    """
    db_session.add(model_class(**row_dict))
    db_session.commit()

    queried_row = db_session.query(model_class).filter_by(id=row_dict["id"]).first()

    for k, v in row_dict.items():
        assert queried_row.__dict__[k] == v
