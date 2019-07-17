import pytest
import urwid
import polka

from polka_curses.views.books_page import BooksPage, BookItem


@pytest.fixture
def bookpage():
    return BooksPage(polka.books())


@pytest.fixture
def bookitem(bookpage):
    book = bookpage.books[0]
    return BookItem(book)


def test_get_books_from_page(bookpage):
    assert bookpage.books


def test_get_focused_book(bookpage):
    first_focused = bookpage.get_focused_book()
    bookpage.set_focus(1)
    second_focused = bookpage.get_focused_book()
    assert isinstance(first_focused, polka.Book)
    assert isinstance(second_focused, polka.Book)
    assert first_focused != second_focused


def test_get_book_from_item(bookitem):
    assert isinstance(bookitem.book, polka.Book)


def test_book_item_is_selectable(bookitem):
    assert bookitem.selectable()
