import json
import pytest
from unittest.mock import MagicMock, patch
from src.ai_provider.openai_provider.open_ai_provider import OpenAIProvider
from src.handlers.reddit.comment.classify_temporal_handler import (
    ClassifyTemporalHandler,
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
        "mbomop8": {"start_date": "2025-06-10", "end_date": "2025-06-10"},
        "mbr1lyf": {"start_date": "2025-07-01", "end_date": "2025-07-15"},
        "mba3rta": {"start_date": None, "end_date": None},
    }
    with patch.object(
        ClassifyTemporalHandler,
        "query_and_load_json",
        return_value=mock_query_result,
    ):
        handler = ClassifyTemporalHandler(ai_provider=mock_ai_provider)

        result_data = handler.do_handle(input_data)

        result_json = json.loads(result_data)

        assert result_json[0]["start_date"] == "2025-06-10"
        assert result_json[0]["end_date"] == "2025-06-10"

        assert result_json[1]["start_date"] == "2025-07-01"
        assert result_json[1]["end_date"] == "2025-07-15"

        assert result_json[2]["start_date"] is None
        assert result_json[2]["end_date"] is None
