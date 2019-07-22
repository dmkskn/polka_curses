import pytest
import urwid
import polka

from polka_curses.views.books_page import BooksPage, BookItem


@pytest.fixture
def bookspage(books):
    return BooksPage(books)


@pytest.fixture
def bookitem(book):
    return BookItem(book)


def test_get_books_from_page(bookspage):
    assert bookspage.books


def test_get_focused_book(bookspage):
    first_focused = bookspage.get_focused_book()
    bookspage.set_focus(1)
    second_focused = bookspage.get_focused_book()
    assert isinstance(first_focused, polka.Book)
    assert isinstance(second_focused, polka.Book)
    assert first_focused != second_focused


def test_get_book_from_item(bookitem, model):
    assert model.is_book(bookitem.book)


def test_book_item_is_selectable(bookitem):
    assert bookitem.selectable()
