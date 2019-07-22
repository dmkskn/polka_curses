import pytest

from polka_curses.views.experts_page import ExpertsPage, ExpertItem


@pytest.fixture
def expertspage(experts):
    return ExpertsPage(experts)


@pytest.fixture
def expertitem(expert):
    return ExpertItem(expert)


def test_get_expertss_from_page(expertspage):
    assert expertspage.experts


def test_get_focused_book(expertspage, model):
    first_focused = expertspage.get_focused_expert()
    expertspage.set_focus(1)
    second_focused = expertspage.get_focused_expert()
    assert model.is_expert(first_focused)
    assert model.is_expert(second_focused)
    assert first_focused != second_focused


def test_get_book_from_item(expertitem, model):
    assert model.is_expert(expertitem.expert)


def test_book_item_is_selectable(expertitem):
    assert expertitem.selectable()
