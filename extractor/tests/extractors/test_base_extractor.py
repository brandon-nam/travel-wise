import pytest

from src.extractors.base_extractor import BaseExtractor


def test_base_extractor_raises_when_instantiated():
    with pytest.raises(TypeError):
        BaseExtractor()
