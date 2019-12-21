import pytest
import urwid

from polka_curses.views.tab_bar import TabBar


FIRST_INDEX = 0
LAST_INDEX = 5


@pytest.fixture(scope="function")
def tabbar():
    return TabBar(FIRST_INDEX)


def test_build(tabbar):
    w = tabbar._build()
    assert isinstance(w, urwid.AttrMap)
    assert isinstance(w.base_widget, urwid.Text)


def test_is_valid_index(tabbar):
    for i in range(FIRST_INDEX, LAST_INDEX + 1):
        assert tabbar._is_valid_index(i)
    assert not tabbar._is_valid_index(FIRST_INDEX - 1)
    assert not tabbar._is_valid_index(LAST_INDEX + 1)
    assert not tabbar._is_valid_index(LAST_INDEX + 2)


def test_set_tab(tabbar):
    for i in range(FIRST_INDEX, LAST_INDEX):
        try:
            tabbar.set_tab(i)
            assert tabbar.index == i
        except IndexError:
            m = f"The index {i} is correct, but it is not possible to set the tab"
            assert False, m


def test_set_tab_with_wrong_index(tabbar):
    with pytest.raises(IndexError):
        tabbar.set_tab(FIRST_INDEX - 1)
    with pytest.raises(IndexError):
        tabbar.set_tab(LAST_INDEX + 1)


def test_get_current_tab(tabbar):
    tabbar.set_tab(0)
    assert tabbar.get_current_tab() == "КНИГИ"
    tabbar.set_tab(1)
    assert tabbar.get_current_tab() == "СПИСКИ"
    tabbar.set_tab(2)
    assert tabbar.get_current_tab() == "ЭКСПЕРТЫ"
    tabbar.set_tab(3)
    assert tabbar.get_current_tab() == "ПОДКАСТЫ"
    tabbar.set_tab(4)
    assert tabbar.get_current_tab() == "СТАТЬИ"
    tabbar.set_tab(5)
    assert tabbar.get_current_tab() == "ПОИСК"


def test_is_first_index(tabbar):
    tabbar.set_tab(FIRST_INDEX)
    assert tabbar.is_first_index()
    assert not tabbar.is_last_index()


def test_is_last_index(tabbar):
    tabbar.set_tab(LAST_INDEX)
    assert tabbar.is_last_index()
    assert not tabbar.is_first_index()
