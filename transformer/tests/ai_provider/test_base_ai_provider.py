import pytest
from src.ai_provider.base_ai_provider import BaseAIProvider


def test_base_ai_provider_cannot_be_instantiated():
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class BaseAIProvider without an implementation for abstract method 'prompt'",
    ):
        BaseAIProvider()
