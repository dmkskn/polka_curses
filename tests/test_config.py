import pytest
import polka_curses.config as config
from polka_curses.config import Key, Mode, Palette, KEYS
from polka_curses.controller import ViewController

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


def test_get_key_action(monkeypatch, TEST_KEYS):
    monkeypatch.setattr(config, "KEYS", TEST_KEYS)
    assert config.get_key_action(Mode.BOOKS_PAGE, "esc") == "test_exit"


def test_get_mode_by_raw_value():
    assert Mode.get("КНИГИ") == Mode.BOOKS_PAGE
    assert Mode.get("НЕ СУЩЕСТВУЕТ") is None


def test_help_for_mode(monkeypatch, TEST_KEYS):
    monkeypatch.setattr(config, "KEYS", TEST_KEYS)
    result = config.help_string_for(Mode.BOOKS_PAGE)
    assert result == TEST_HELP_STRING_FOR_BOOKS_PAGE


def test_keys_actions_exists():
    actions = [k.action for k in KEYS]
    controller = ViewController()
    for action in actions:
        assert action in dir(controller)
