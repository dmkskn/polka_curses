import pytest

import polka_curses.config as config
from polka_curses.config import Key, Mode, Palette


TEST_HELP_STRING_FOR_BOOKS_PAGE = "ОТКРЫТЬ (Enter), ВЫХОД (Esc)"


@pytest.fixture
def TEST_KEYS():
    return [
        Key(
            name="Left",
            description="ВЛЕВО",
            buttons=["left"],
            action="test_move_left",
            modes=Mode.tabs(),
            hidden=True,
        ),
        Key(
            name="Enter",
            description="ОТКРЫТЬ",
            buttons=["enter"],
            action="test_open_book",
            modes=Mode.tabs(),
        ),
        Key(
            name="Esc",
            description="ВЫХОД",
            buttons=["esc"],
            action="test_exit",
            modes=Mode.tabs(),
        ),
    ]


def test_palette_is_tuple():
    assert issubclass(Palette, tuple)


def test_key_is_tuple():
    assert issubclass(Key, tuple)


def test_get_key_action(TEST_KEYS):
    KEYS = config.KEYS
    config.KEYS = TEST_KEYS
    assert config.get_key_action(Mode.BOOKS_PAGE, "esc") == "test_exit"
    config.KEYS = KEYS


def test_get_mode_by_raw_value():
    assert Mode.get("КНИГИ") == Mode.BOOKS_PAGE
    assert Mode.get("НЕ СУЩЕСТВУЕТ") is None


def test_help_for_mode(TEST_KEYS):
    KEYS = config.KEYS
    config.KEYS = TEST_KEYS
    result = config.help_string_for(Mode.BOOKS_PAGE)
    assert result == TEST_HELP_STRING_FOR_BOOKS_PAGE
    config.KEYS = KEYS
