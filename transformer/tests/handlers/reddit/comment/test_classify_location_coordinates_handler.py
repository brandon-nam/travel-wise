import json
import pytest
from unittest.mock import MagicMock, patch
from src.ai_provider.openai_provider.open_ai_provider import OpenAIProvider

from src.handlers.reddit.comment.classify_location_coordinates_handler import (
    ClassifyLocationCoordinatesHandler,
)


@pytest.fixture
def mock_ai_provider():
    return MagicMock(spec=OpenAIProvider)


def test_do_handle():

    input_data = """
    [
        {"id": "mbomop8", "text": "I visited Tokyo and Universal Studios Japan."},
        {"id": "mbr1lyf", "text": "The Wagyu at Wagyu Idaten was amazing! Also visited Ghibli Museum."},
        {"id": "mba3rta", "text": "No location here!"}
    ]
    """

    mock_query_result = {
        "mbomop8": [
            {
                "lat": 35.3192,
                "lng": 139.5467,
                "location_name": "Tokyo",
                "characteristic": "city",
            },
            {
                "lat": 35.4449,
                "lng": 139.6368,
                "location_name": "Universal Studios Japan",
                "characteristic": "theme park",
            },
        ],
        "mbr1lyf": [
            {
                "lat": 35.7719,
                "lng": 140.3929,
                "location_name": "Wagyu Idaten",
                "characteristic": "restaurant",
            },
            {
                "lat": 35.0116,
                "lng": 135.7681,
                "location_name": "Ghibli Museum",
                "characteristic": "museum",
            },
        ],
        "mba3rta": [],
    }

    mock_ai_provider = MagicMock()

    with patch.object(
        ClassifyLocationCoordinatesHandler,
        "query_and_load_json",
        return_value=mock_query_result,
    ):
        handler = ClassifyLocationCoordinatesHandler(ai_provider=mock_ai_provider)

        result_data = handler.do_handle(input_data)

        result_json = json.loads(result_data)

        assert result_json[0]["locations"] == [
            {
                "lat": 35.3192,
                "lng": 139.5467,
                "location_name": "Tokyo",
                "characteristic": "city",
            },
            {
                "lat": 35.4449,
                "lng": 139.6368,
                "location_name": "Universal Studios Japan",
                "characteristic": "theme park",
            },
        ]

        assert result_json[1]["locations"] == [
            {
                "lat": 35.7719,
                "lng": 140.3929,
                "location_name": "Wagyu Idaten",
                "characteristic": "restaurant",
            },
            {
                "lat": 35.0116,
                "lng": 135.7681,
                "location_name": "Ghibli Museum",
                "characteristic": "museum",
            },
        ]

        assert result_json[2]["locations"] == []
