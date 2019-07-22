import pytest
import urwid

from polka_curses.view import ViewError
from polka_curses.views.book_page import BookPage
from polka_curses.views.books_page import BooksPage
from polka_curses.views.expert_page import ExpertPage
from polka_curses.views.experts_page import ExpertsPage
from polka_curses.views.list_page import ListPage, ListDescription
from polka_curses.views.lists_page import ListsPage
from polka_curses.views.search_page import SearchPage, SearchResultItem


LEFT_MESSAGE = "left"
RIGHT_MESSAGE = "right"
TEST_QUERY = "test"


def test_set_body(view):
    view.set_body(urwid.Text(""))
    assert isinstance(view.body, urwid.Text)


def test_set_header(view):
    view.set_header(urwid.Text(""))
    assert isinstance(view.header, urwid.Text)


def test_set_footer(view):
    view.set_footer(urwid.Text(""))
    assert isinstance(view.footer, urwid.Text)


def test_draw_books(view, books):
    view.draw_books(books, LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, BooksPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_lists(view, lists):
    view.draw_lists(lists, LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, ListsPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_experts(view, experts):
    view.draw_experts(experts, LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, ExpertsPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_search(view):
    view.draw_search(LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, SearchPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_list_description(view, lists):
    view.draw_lists(lists)
    view.draw_list(view.get_focused_list())
    view.draw_list_description(LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, ListDescription)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_list_description_not_in_list_page(view, books):
    view.draw_books(books)
    with pytest.raises(ViewError):
        view.draw_list_description()


def test_get_search_query(view):
    view.draw_search()
    assert view.get_search_query() == ""
    view.body.search.edit_text = TEST_QUERY
    assert view.get_search_query() == TEST_QUERY


def test_get_search_query_if_the_current_page_is_not_search_page(view):
    with pytest.raises(ViewError):
        _ = view.get_search_query()


def test_focus_next_tab(view):
    if view.header.is_last_index():
        view.focus_previous_tab()
        i = view.header.index
    else:
        i = view.header.index
    view.focus_next_tab()
    assert view.header.index == i + 1


def test_focus_next_tab_if_there_is_no_tab_bar(view, book):
    view.draw_book(book)
    with pytest.raises(ViewError):
        view.focus_next_tab()


def test_focus_previous_tab(view):
    if view.header.is_first_index():
        view.focus_next_tab()
        i = view.header.index
    else:
        i = view.header.index
    view.focus_previous_tab()
    assert view.header.index == i - 1


def test_focus_previous_tab_if_there_is_no_tab_bar(view, book):
    view.draw_book(book)
    with pytest.raises(ViewError):
        view.focus_previous_tab()


def test_draw_book(view, book):
    view.draw_book(book, LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, BookPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_list(view, list_):
    view.draw_list(list_, LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, ListPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_draw_expert(view, expert):
    view.draw_expert(expert, LEFT_MESSAGE, RIGHT_MESSAGE)
    assert isinstance(view.body, ExpertPage)
    assert view.footer.left == LEFT_MESSAGE
    assert view.footer.right == RIGHT_MESSAGE


def test_write_error_the_book_has_no_page(view, book):
    view.write_error_the_book_has_no_page(book)
    assert view.footer.left == f"Нет статьи на книгу «{book.title.upper()}»"


def test_saves_previous(view, book):
    view.draw_book(book)
    assert view.previous_bodies
    assert view.previous_footers
    assert view.previous_headers


def test_draw_previous(view, book):
    body = view.body
    header = view.header
    footer = view.footer
    view.draw_book(book)
    assert body != view.body
    assert header != view.header
    assert footer != view.footer
    view.draw_previous()
    assert body == view.body
    assert header == view.header
    assert footer == view.footer


def test_get_focused_list(view, lists, model):
    view.draw_lists(lists)
    assert model.is_list(view.get_focused_list())


def test_get_focused_list_not_in_lists_page(view):
    with pytest.raises(ViewError):
        view.get_focused_list()


def test_get_focused_book(view, books, model):
    view.draw_books(books)
    assert model.is_book(view.get_focused_book())


def test_get_focused_book_not_in_books_page(view):
    view.draw_book(view.get_focused_book())
    with pytest.raises(ViewError):
        view.get_focused_book()


def test_get_focused_expert(view, experts, model):
    view.draw_experts(experts)
    assert model.is_expert(view.get_focused_expert())


def test_get_focused_expert_not_in_experts_page(view, books):
    view.draw_books(books)
    with pytest.raises(ViewError):
        view.get_focused_expert()


def test_get_focused_search_result(view, model):
    view.show_search_results(model.search("грибоедов"))
    result = view.get_focused_search_result()
    is_book = model.is_book(result)
    is_list = model.is_list(result)
    is_expert = model.is_expert(result)
    assert is_book or is_list or is_expert


def test_get_focused_search_result_not_in_search_result_page(view, books):
    view.draw_books(books)
    with pytest.raises(ViewError):
        view.get_focused_search_result()
