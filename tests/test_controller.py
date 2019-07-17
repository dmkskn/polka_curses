import pytest
import urwid

from polka_curses.controller import ViewController
from polka_curses.view import View
from polka_curses.model import Model


@pytest.fixture(scope="function")
def controller():
    return ViewController(View, Model)


def test_exit(controller):
    with pytest.raises(urwid.ExitMainLoop):
        controller.exit()
