from unittest.mock import MagicMock
from src.ai_provider.openai_provider.open_ai_provider import OpenAIProvider


def test_prompt(mocker):
    mock_openai = mocker.patch("openai.OpenAI")

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Mock response"))]

    mock_openai.return_value.chat.completions.create.return_value = mock_response

    provider = OpenAIProvider()

    query = "What is the capital of Japan?"
    result = provider.prompt(query)
    mock_openai.return_value.chat.completions.create.assert_called_once()

    assert result == "Mock response"
