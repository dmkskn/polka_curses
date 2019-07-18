import pytest
import polka

from polka_curses.views.lists_page import ListsPage, ListItem


@pytest.fixture
def listspage():
    return ListsPage(polka.lists())


@pytest.fixture
def listitem(listspage):
    list_ = listspage.lists[0]
    return ListItem(list_)


def test_get_lists_from_page(listspage):
    assert listspage.lists


def test_get_focused_list(listspage):
    first_focused = listspage.get_focused_list()
    listspage.set_focus(1)
    second_focused = listspage.get_focused_list()
    assert isinstance(first_focused, polka.Compilation)
    assert isinstance(second_focused, polka.Compilation)
    assert first_focused != second_focused


def test_get_list_from_item(listitem):
    assert isinstance(listitem.list_, polka.Compilation)


def test_book_item_is_selectable(listitem):
    assert listitem.selectable()
