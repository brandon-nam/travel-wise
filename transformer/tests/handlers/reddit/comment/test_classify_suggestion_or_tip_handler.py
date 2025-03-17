import json
import pytest
from unittest.mock import MagicMock, patch
from src.ai_provider.openai_provider.open_ai_provider import OpenAIProvider
from src.handlers.reddit.comment.classify_suggestion_or_tip_handler import (
    ClassifySuggestionOrTipHandler,
)


@pytest.fixture
def mock_ai_provider():
    return MagicMock(spec=OpenAIProvider)


def test_do_handle():

    input_data = """
    [
        {"id": "mhsrrkt", "body": "I'm going to Japan, any tips?"},
        {"id": "mhwc6o5", "body": "What's the best way to get around Tokyo?"}
    ]
    """

    mock_query_result = {
        "mhsrrkt": {"classification": "travel_tip", "characteristic": "advice"},
        "mhwc6o5": {
            "classification": "travel_suggestion",
            "characteristic": "transport",
        },
    }

    mock_ai_provider = MagicMock()

    with patch.object(
        ClassifySuggestionOrTipHandler,
        "query_and_load_json",
        return_value=mock_query_result,
    ):
        handler = ClassifySuggestionOrTipHandler(ai_provider=mock_ai_provider)

        result_data = handler.do_handle(input_data)

        result_json = json.loads(result_data)

        assert result_json[0]["classification"] == "travel_tip"
        assert result_json[0]["characteristic"] == "advice"

        assert result_json[1]["classification"] == "travel_suggestion"
        assert result_json[1]["characteristic"] == "transport"
