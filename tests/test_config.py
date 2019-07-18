import pytest

from polka_curses.config import Palette, Key, Mode, PALETTE, get_key_action


def test_palette_is_tuple():
    assert issubclass(Palette, tuple)


def test_key_is_tuple():
    assert issubclass(Key, tuple)


def test_get_key_action():
    assert get_key_action(Mode.BOOKS_PAGE, "esc") == "exit"
