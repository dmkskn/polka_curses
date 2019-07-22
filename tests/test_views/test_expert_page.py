import pytest

from polka_curses.views.expert_page import ExpertPage


@pytest.fixture(scope="module")
def expert_page_full(experts):
    """Has favorite books and wrote articles"""
    experts = [e for e in experts if e.favorites and e.wrote_about]
    if experts:
        return ExpertPage(experts[0])
    else:
        return None


@pytest.fixture(scope="module")
def expert_page_favs(experts):
    """Only favorite books. Wrote no articles."""
    experts = [e for e in experts if e.favorites and not e.wrote_about]
    if experts:
        return ExpertPage(experts[0])
    else:
        return None


@pytest.fixture(scope="module")
def expert_page_wrote(experts):
    """No favorite books. Wrote articles."""
    experts = [e for e in experts if not e.favorites and e.wrote_about]
    if experts:
        return ExpertPage(experts[0])
    else:
        return None


def test_is_two_columns_arg(expert_page_full, expert_page_favs):
    if expert_page_full:
        assert expert_page_full.is_two_columns
    if expert_page_favs:
        assert not expert_page_favs.is_two_columns


def test_get_focused_column_when_two_of_them(expert_page_full):
    if expert_page_full:
        expert = expert_page_full
        assert expert.get_focused_column() is expert.favorites
        expert.container.focus_position = 1
        assert expert.get_focused_column() is expert.wrote_about


def test_get_focused_column_when_only_one(expert_page_favs, expert_page_wrote):
    e1, e2 = expert_page_favs, expert_page_wrote
    if e1:
        assert e1.get_focused_column() is e1.favorites
    if e2:
        assert e2.get_focused_column() is e2.wrote_about


def test_get_focused_book_if_expert_is_full(expert_page_full, model):
    if expert_page_full:
        assert model.is_book(expert_page_full.get_focused_book())


def test_get_focused_book_if_expert_has_only_favs(expert_page_favs, model):
    if expert_page_favs:
        assert model.is_book(expert_page_favs.get_focused_book())


def test_get_focused_book_if_expert_only_wrote(expert_page_wrote, model):
    if expert_page_wrote:
        assert model.is_book(expert_page_wrote.get_focused_book())
