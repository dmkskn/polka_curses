import pytest

from polka_curses.views.lists_page import ListsPage, ListItem


@pytest.fixture
def listspage(lists):
    return ListsPage(lists)


@pytest.fixture
def listitem(listspage):
    list_ = listspage.lists[0]
    return ListItem(list_)


def test_get_lists_from_page(listspage):
    assert listspage.lists


def test_get_focused_list(listspage, model):
    first_focused = listspage.get_focused_list()
    listspage.set_focus(1)
    second_focused = listspage.get_focused_list()
    assert model.is_list(first_focused)
    assert model.is_list(second_focused)
    assert first_focused != second_focused


def test_get_list_from_item(listitem, model):
    assert model.is_list(listitem.list_)


def test_book_item_is_selectable(listitem):
    assert listitem.selectable()
