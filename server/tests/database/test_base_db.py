import pytest

from src.database.base_db import BaseDB


def test_base_db_cannot_be_instantiated():
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class BaseDB without an implementation for abstract methods 'get_comments', 'get_posts', 'setup_db'",
    ):
        BaseDB("mock_uri")
