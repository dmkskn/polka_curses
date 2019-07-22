import pytest
import urwid

from unittest.mock import MagicMock, patch

from polka_curses.controller import ViewController

from polka_curses.views.books_page import BooksPage
from polka_curses.views.lists_page import ListsPage
from polka_curses.views.experts_page import ExpertsPage
from polka_curses.views.search_page import SearchPage, SearchResultsPage

from polka_curses.config import Mode, help_string_for


@pytest.fixture()
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


def test_open_book(controller, book):
    controller.view = MagicMock()
    controller.view.get_focused_book = MagicMock(return_value=book)
    controller.open_book()
    assert controller.view.draw_book.called
    assert controller.view.draw_book.call_args[0][0] == book
    assert controller.mode == Mode.BOOK_PAGE


def test_open_book_that_doesnt_have_article(controller, books):
    books = [_ for _ in books if not _.has_article]
    if not books:
        return None
    book = books[0]
    controller.view = MagicMock()
    controller.view.get_focused_book = MagicMock(return_value=book)
    controller.open_book()
    assert not controller.view.draw_book.called
    assert controller.view.write_error_the_book_has_no_page.called
    arg = controller.view.write_error_the_book_has_no_page.call_args[0][0]
    assert arg == book
    assert controller.mode == Mode.BOOKS_PAGE


def test_open_list(controller, list_):
    controller.view = MagicMock()
    controller.view.get_focused_list = MagicMock(return_value=list_)
    controller.open_list()
    assert controller.view.draw_list.called
    assert controller.view.draw_list.call_args[0][0] == list_
    assert controller.mode == Mode.LIST_PAGE


def test_open_expert(controller, expert):
    controller.view = MagicMock()
    controller.view.get_focused_expert = MagicMock(return_value=expert)
    controller.open_expert()
    assert controller.view.draw_expert.called
    assert controller.view.draw_expert.call_args[0][0] == expert
    assert controller.mode == Mode.EXPERT_PAGE


def test_open_list_description(controller):
    controller.view = MagicMock()
    controller.show_list_description()
    assert controller.view.draw_list_description.called
    assert controller.mode == Mode.LIST_DESCRIPTION_PAGE


def test_saves_last_mode(controller):
    assert not controller.last_mode
    controller.view = MagicMock()
    controller.open_book()
    assert controller.last_mode


def test_open_previous(controller):
    controller.view.draw_previous = MagicMock()
    controller.open_book()
    assert controller.mode == Mode.BOOK_PAGE
    controller.open_previous()
    assert controller.view.draw_previous.called
    assert controller.mode != Mode.BOOK_PAGE


def test_open_in_browser(controller):
    controller.view = MagicMock()

    controller.open_book()
    with patch("webbrowser.open") as mock_webbrowser:
        controller.open_in_browser()
        assert mock_webbrowser.called
        assert controller.view.get_book_article_url.called

    controller.open_list()
    with patch("webbrowser.open") as mock_webbrowser:
        controller.open_in_browser()
        assert mock_webbrowser.called
        assert controller.view.get_list_article_url.called

    controller.open_expert()
    with patch("webbrowser.open") as mock_webbrowser:
        controller.open_in_browser()
        assert mock_webbrowser.called
        assert controller.view.get_expert_article_url.called


def test_open_search_result(controller, book, list_, expert):
    controller.view = MagicMock()

    controller.view.get_focused_search_result = MagicMock(return_value=book)
    controller.open_search_result()
    assert controller.view.draw_book.call_args[0][0] == book
    assert controller.mode == Mode.BOOK_PAGE

    controller.view.get_focused_search_result = MagicMock(return_value=list_)
    controller.open_search_result()
    assert controller.view.draw_list.call_args[0][0] == list_
    assert controller.mode == Mode.LIST_PAGE

    controller.view.get_focused_search_result = MagicMock(return_value=expert)
    controller.open_search_result()
    assert controller.view.draw_expert.call_args[0][0] == expert
    assert controller.mode == Mode.EXPERT_PAGE
