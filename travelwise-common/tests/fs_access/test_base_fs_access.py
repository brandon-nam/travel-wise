import pytest

from fs_access.base_fs_access import BaseFSAccess


def test_cannot_instantiate_base_fs_access():
    with pytest.raises(TypeError):
        BaseFSAccess()
