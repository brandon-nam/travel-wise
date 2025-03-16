import pytest

from src.collectors.collector import Collector


def test_cannot_instantiate_collector():
    with pytest.raises(TypeError):
        Collector()
