import pytest

from polka_curses.views.loading_page import LoadingPage


@pytest.fixture
def loading_page():
    return LoadingPage()


def test_update(loading_page):
    assert loading_page.text == loading_page.emoji[0]
    loading_page.update()
    assert loading_page.text == loading_page.emoji[1]
    loading_page.update()
    assert loading_page.text == loading_page.emoji[2]
    loading_page.update()
    assert loading_page.text == loading_page.emoji[0]
