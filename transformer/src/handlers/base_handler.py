import logging
from abc import ABC, abstractmethod
from typing import Self

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BaseHandler(ABC):
    _next_handler: Self = None

    @staticmethod
    def setup_handler_chain(handlers: list[Self]) -> None:
        for i in range(len(handlers) - 1):
            handlers[i].set_next(handlers[i + 1])

    def set_next(self, handler: Self) -> Self:
        self._next_handler = handler
        return handler

    def handle(self, input_data: str) -> str:
        logger.info(
            f"Current handler: {self.__class__.__name__}, next handler: {self._next_handler.__class__.__name__}"
        )
        handled_input = self.do_handle(input_data)
        if self._next_handler is not None:
            return self._next_handler.handle(handled_input)
        else:
            return handled_input

    @abstractmethod
    def do_handle(self, input_data):
        raise NotImplementedError()
