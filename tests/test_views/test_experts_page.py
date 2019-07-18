import pytest
import polka

from polka_curses.views.experts_page import ExpertsPage, ExpertItem


@pytest.fixture
def expertspage():
    return ExpertsPage(polka.pundits())


@pytest.fixture
def expertitem(expertspage):
    expert = expertspage.experts[0]
    return ExpertItem(expert)


def test_get_expertss_from_page(expertspage):
    assert expertspage.experts


def test_get_focused_book(expertspage):
    first_focused = expertspage.get_focused_expert()
    expertspage.set_focus(1)
    second_focused = expertspage.get_focused_expert()
    assert isinstance(first_focused, polka.Pundit)
    assert isinstance(second_focused, polka.Pundit)
    assert first_focused != second_focused


def test_get_book_from_item(expertitem):
    assert isinstance(expertitem.expert, polka.Pundit)


def test_book_item_is_selectable(expertitem):
    assert expertitem.selectable()
