from unittest.mock import MagicMock
from src.transformers.base_transformer import BaseTransformer
from src.handlers.base_handler import BaseHandler
from fs_access.base_fs_access import BaseFSAccess


class MockTransformer(BaseTransformer):
    def __init__(self, fs_access):
        super().__init__(fs_access)

    @property
    def chain(self):
        return [MagicMock(spec=BaseHandler), MagicMock(spec=BaseHandler)]

    def transform(self):
        pass


def test_base_transformer_init():
    mock_fs = MagicMock(spec=BaseFSAccess)
    transformer = MockTransformer(mock_fs)

    assert transformer.fs_access == mock_fs
    assert len(transformer.chain) == 2


def test_chain():
    mock_fs = MagicMock(spec=BaseFSAccess)
    transformer = MockTransformer(mock_fs)

    assert isinstance(transformer.chain, list)
    assert all(isinstance(handler, BaseHandler) for handler in transformer.chain)
