import pytest
from unittest.mock import MagicMock

from polka_curses.handler import InputHandler
from polka_curses.controller import ViewController
from polka_curses.config import Mode


@pytest.fixture(scope="function")
def controller():
    mock_controller = MagicMock(ViewController)
    mock_controller.mode = Mode.BOOKS_PAGE
    return mock_controller


@pytest.fixture
def handler(controller):
    return InputHandler(controller)


def test_handle_finds_action_and_call_do(handler):
    handler.do = MagicMock()
    handler.handle("esc")
    args, _ = handler.do.call_args
    assert args == ("exit",)


def test_do_calls_controller_action_method(handler, controller):
    handler.do("exit")
    assert controller.exit.called
