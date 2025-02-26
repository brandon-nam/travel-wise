import pytest

from writers.base_writer import BaseWriter


def test_base_writer_cannot_be_instantiated():
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class BaseWriter without an implementation for abstract method 'write_json'",
    ):
        BaseWriter()
