import pytest
import urwid

from polka_curses.views.status_bar import StatusBar


TEXT = "New text"


@pytest.fixture(scope="function")
def statusbar():
    return StatusBar()


def test_get_left(statusbar):
    assert statusbar.left == ""


def test_get_right(statusbar):
    assert statusbar.right == ""


def test_get_cols(statusbar):
    assert isinstance(statusbar.cols[0], urwid.Text)
    assert isinstance(statusbar.cols[1], urwid.Text)


def test_set_left(statusbar):
    statusbar.set_left(TEXT)
    assert statusbar.left == TEXT


def test_set_right(statusbar):
    statusbar.set_right(TEXT)
    assert statusbar.right == TEXT


def test_clear_left(statusbar):
    statusbar.set_left(TEXT)
    statusbar.clear_left()
    assert statusbar.left == ""


def test_clear_right(statusbar):
    statusbar.set_left(TEXT)
    statusbar.clear_left()
    assert statusbar.right == ""
