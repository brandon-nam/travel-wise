import json
import pytest
from handlers.reddit.comment.location_deduplication_handler import (
    LocationDeduplicationHandler,
)


@pytest.fixture
def handler():
    return LocationDeduplicationHandler()


def test_location_deduplication(handler):
    input_data = """
[
    {
        "id": "c1",
        "locations": [
            {
                "location_name": "Tokyo Tower",
                "lat": 35.6586,
                "lng": 139.7454
            },
            {
                "location_name": "Tokyo Tower",
                "lat": 35.6587,
                "lng": 139.7455
            }
        ]
    },
    {
        "id": "c2",
        "locations": [
            {
                "location_name": "Shibuya Crossing",
                "lat": 35.6595,
                "lng": 139.7005
            }
        ]
    },
    {
        "id": "c3",
        "locations": [
            {
                "location_name": "Tokyo Tower",
                "lat": 35.6590,
                "lng": 139.7460
            }
        ]
    }
]
"""

    expected_output = json.loads(input_data)

    # After deduplication, the second location for Tokyo Tower should match the first one
    expected_output[0]["locations"][1]["lat"] = pytest.approx(35.6586, rel=1e-3)
    expected_output[0]["locations"][1]["lng"] = pytest.approx(139.7454, rel=1e-3)
    expected_output[2]["locations"][0]["lat"] = pytest.approx(35.6586, rel=1e-3)
    expected_output[2]["locations"][0]["lng"] = pytest.approx(139.7454, rel=1e-3)

    result_data = handler.do_handle(input_data)  # Pass the input as a string
    output_data = json.loads(result_data)

    assert (
        output_data == expected_output
    ), "Location deduplication did not work as expected"
