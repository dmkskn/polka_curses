import pytest
import urwid

from polka_curses.view import View
from polka_curses.model import Model
from polka_curses.views.books_page import BooksPage
from polka_curses.views.lists_page import ListsPage
from polka_curses.views.experts_page import ExpertsPage
from polka_curses.views.search_page import SearchPage
from polka_curses.views.book_page import BookPage
from polka_curses.views.list_page import ListPage
from polka_curses.views.expert_page import ExpertPage


LEFT_MESSAGE = "left"
RIGHT_MESSAGE = "right"
TEST_QUERY = "test"


@pytest.fixture
def model():
    return Model()


@pytest.fixture
def view(model):
    return View(model.books)


def test_set_body(view):
    view.set_body(urwid.Text(""))
    assert isinstance(view.body, urwid.Text)


def test_set_header(view):
    view.set_header(urwid.Text(""))
    assert isinstance(view.header, urwid.Text)


def test_set_footer(view):
    view.set_footer(urwid.Text(""))
    assert isinstance(view.footer, urwid.Text)


def test_draw_books(view, model):
    view.draw_books(model.books, LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, BooksPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_lists(view, model):
    view.draw_lists(model.lists, LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, ListsPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_experts(view, model):
    view.draw_experts(model.experts, LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, ExpertsPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_search(view):
    view.draw_search(LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, SearchPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_get_search_query(view):
    view.draw_search()
    assert view.get_search_query() == ""
    view.body.search.edit_text = TEST_QUERY
    assert view.get_search_query() == TEST_QUERY


def test_focus_next_tab(view):
    if view.header.is_last_index():
        view.focus_previous_tab()
        i = view.header.index
    else:
        i = view.header.index
    view.focus_next_tab()
    assert view.header.index == i + 1


def test_focus_previous_tab(view):
    if view.header.is_first_index():
        view.focus_next_tab()
        i = view.header.index
    else:
        i = view.header.index
    view.focus_previous_tab()
    assert view.header.index == i - 1


def test_draw_book(view, model):
    view.draw_book(model.books[0], LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, BookPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_list(view, model):
    view.draw_list(model.lists[0], LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, ListPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_expert(view, model):
    view.draw_expert(model.experts[0], LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, ExpertPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_write_error_the_book_has_no_page(view, model):
    book = model.books[0]
    view.write_error_the_book_has_no_page(book)
    assert view.footer.left == f"Нет статьи на книгу «{book.title.upper()}»"
