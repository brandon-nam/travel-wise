from abc import ABC, abstractmethod

from fs_access.base_fs_access import BaseFSAccess
from handlers.base_handler import BaseHandler


class BaseTransformer(ABC):
    def __init__(self, fs_access: BaseFSAccess) -> None:
        BaseHandler.setup_handler_chain(self.chain)
        self.fs_access = fs_access

    @property
    def chain(self) -> list[BaseHandler]:
        raise NotImplementedError()

    @abstractmethod
    def transform(self) -> None:
        raise NotImplementedError()

