import pytest

from polka_curses.views.list_page import ListPage, BookInListItem
from polka_curses.model import Model


@pytest.fixture
def model():
    return Model()


@pytest.fixture
def listpage(model):
    list_ = model.lists[0]
    return ListPage(list_)


@pytest.fixture
def bookitem(listpage):
    return BookInListItem(listpage.list_.books[0])


def test_get_list_from_page(listpage):
    assert listpage.list_


def test_get_focused_book(listpage, model):
    first_focused = listpage.get_focused_book()
    listpage.set_focus(1)
    second_focused = listpage.get_focused_book()
    assert model.is_book(first_focused)
    assert model.is_book(second_focused)
    assert first_focused != second_focused


def test_get_book_from_item(bookitem, model):
    assert model.is_book(bookitem.book)


def test_book_item_is_selectable(bookitem):
    assert bookitem.selectable()
