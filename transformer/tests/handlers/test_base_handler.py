import pytest
from src.handlers.base_handler import BaseHandler


class MockHandler(BaseHandler):
    def do_handle(self, input_data):
        return f"processed: {input_data}"


@pytest.fixture
def mock_handler(mocker):
    handler = MockHandler()
    mocker.patch.object(handler, "do_handle", return_value="mock result")
    return handler


def test_do_handle_called(mock_handler):
    input_data = "test input"
    mock_handler.handle(input_data)

    mock_handler.do_handle.assert_called_once_with(input_data)


def test_setup_handler_chain(mocker):
    handler1 = MockHandler()
    handler2 = MockHandler()

    mocker.patch.object(handler1, "do_handle", return_value="processed data 1")
    mocker.patch.object(handler2, "do_handle", return_value="processed data 2")

    handler1.set_next(handler2)

    result = handler1.handle("original input")

    handler1.do_handle.assert_called_once_with("original input")
    handler2.do_handle.assert_called_once_with("processed data 1")

    assert result == "processed data 2"


def test_no_next_handler(mock_handler):
    input_data = "test input"
    result = mock_handler.handle(input_data)

    assert result == "mock result"
    mock_handler.do_handle.assert_called_once_with(input_data)


def test_handler_chain_multiple(mocker):
    handler1 = MockHandler()
    handler2 = MockHandler()
    handler3 = MockHandler()

    mocker.patch.object(handler1, "do_handle", return_value="processed data 1")
    mocker.patch.object(handler2, "do_handle", return_value="processed data 2")
    mocker.patch.object(handler3, "do_handle", return_value="final result")

    handler1.set_next(handler2).set_next(handler3)

    result = handler1.handle("original input")

    handler1.do_handle.assert_called_once_with("original input")
    handler2.do_handle.assert_called_once_with("processed data 1")
    handler3.do_handle.assert_called_once_with("processed data 2")

    assert result == "final result"
