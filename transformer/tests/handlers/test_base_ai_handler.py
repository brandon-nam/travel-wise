import pytest
from unittest.mock import MagicMock
from src.ai_provider.base_ai_provider import BaseAIProvider
from src.handlers.base_ai_handler import BaseAIHandler


class MockAIHandler(BaseAIHandler):
    def do_handle(self, input_data: str) -> str:
        return input_data


@pytest.fixture
def mock_ai_provider():
    ai_provider = MagicMock(spec=BaseAIProvider)
    ai_provider.prompt.return_value = '{"key": "value"}'
    return ai_provider


def test_query_and_load_json(mock_ai_provider):
    handler = MockAIHandler(ai_provider=mock_ai_provider)
    prompt = "Test prompt"
    result = handler.query_and_load_json(prompt)
    mock_ai_provider.prompt.assert_called_once_with(prompt)
    expected_result = {"key": "value"}
    assert result == expected_result
