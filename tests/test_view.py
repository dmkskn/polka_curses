import pytest
import polka

from polka_curses.view import View


@pytest.fixture
def view():
    return View(polka.books())
