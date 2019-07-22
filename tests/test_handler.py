import pytest
from unittest.mock import MagicMock

from polka_curses.handler import InputHandler
from polka_curses.config import Mode


@pytest.fixture
def controller_mock(controller):
    controller = MagicMock(controller)
    controller.mode = Mode.BOOKS_PAGE
    return controller


@pytest.fixture
def handler(controller_mock):
    return InputHandler(controller_mock)


def test_handle_finds_action_and_call_do(handler):
    handler.do = MagicMock()
    handler.handle("esc")
    args, _ = handler.do.call_args
    assert args == ("exit",)


def test_do_calls_controller_action_method(handler, controller_mock):
    handler.do("exit")
    assert controller_mock.exit.called
