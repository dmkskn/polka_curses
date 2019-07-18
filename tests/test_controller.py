import pytest
import urwid

from unittest.mock import MagicMock

from polka_curses.controller import ViewController
from polka_curses.view import View
from polka_curses.views.books_page import BooksPage
from polka_curses.views.lists_page import ListsPage
from polka_curses.views.experts_page import ExpertsPage
from polka_curses.views.search_page import SearchPage
from polka_curses.model import Model


@pytest.fixture(scope="function")
def controller():
    return ViewController(View, Model)


def test_exit(controller):
    with pytest.raises(urwid.ExitMainLoop):
        controller.exit()


def test_move_right(controller):
    controller.draw_body_by_tab_name = MagicMock()
    controller.move_right()
    assert controller.draw_body_by_tab_name.called
    arg = controller.draw_body_by_tab_name.call_args[0][0]
    assert isinstance(arg, str)


def test_move_left(controller):
    controller.draw_body_by_tab_name = MagicMock()
    controller.move_left()
    assert controller.draw_body_by_tab_name.called
    arg = controller.draw_body_by_tab_name.call_args[0][0]
    assert isinstance(arg, str)


def test_draw_body_by_tab_name(controller):
    controller.loop = MagicMock()
    view = controller.view
    controller.draw_body_by_tab_name("КНИГИ")
    assert isinstance(view.body, BooksPage)
    controller.draw_body_by_tab_name("СПИСКИ")
    assert isinstance(view.body, ListsPage)
    controller.draw_body_by_tab_name("ЭКСПЕРТЫ")
    assert isinstance(view.body, ExpertsPage)
    controller.draw_body_by_tab_name("ПОИСК")
    assert isinstance(view.body, SearchPage)
    assert controller.loop.draw_screen.called
