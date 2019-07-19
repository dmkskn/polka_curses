import pytest
import urwid

from unittest.mock import MagicMock

from polka_curses.controller import ViewController

from polka_curses.views.books_page import BooksPage
from polka_curses.views.lists_page import ListsPage
from polka_curses.views.experts_page import ExpertsPage
from polka_curses.views.search_page import SearchPage, SearchResultsPage

from polka_curses.config import Mode, help_string_for


@pytest.fixture(scope="function")
def controller():
    controller = ViewController()
    controller.loop = MagicMock()
    return controller


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


def test_add_help_string_when_draw_body(controller):
    view = controller.view
    for mode in Mode.tabs():
        controller.draw_body_by_tab_name(mode.value)
        assert view.footer.right == help_string_for(mode)


def test_show_search(controller):
    controller.view = MagicMock()
    controller.show_search()
    assert controller.view.draw_search.called
    assert controller.loop.draw_screen.called
    assert controller.mode == Mode.SEARCH_PAGE


def test_search(controller):
    controller.show_search()
    controller.view.get_search_query = MagicMock(return_value="грибоедов")
    controller.show_search_results()
    assert isinstance(controller.view.body, SearchResultsPage)
    assert controller.mode == Mode.SEARCH_RESULTS_PAGE
    assert controller.loop.draw_screen.called


def test_search_with_no_results(controller):
    controller.show_search()
    controller.model.search = MagicMock(return_value=[])
    controller.show_search_results()
    assert isinstance(controller.view.body, SearchPage)
    assert controller.view.footer.left == "Нет результатов"
    assert controller.mode == Mode.SEARCH_PAGE
    assert controller.loop.draw_screen.called
