import pytest

from writers.base_writer import BaseWriter


def test_base_writer_cannot_be_instantiated():
    with pytest.raises(
        TypeError,
    ):
        BaseWriter()
