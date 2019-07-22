import pytest
import polka_curses.config as config
from polka_curses.config import Key, Mode, Palette, KEYS
from polka_curses.controller import ViewController

TEST_HELP_STRING_FOR_BOOKS_PAGE = "ОТКРЫТЬ (Enter), ВЫХОД (Esc)"


def test_palette_is_tuple():
    assert issubclass(Palette, tuple)


def test_key_is_tuple():
    assert issubclass(Key, tuple)


def test_get_key_action(monkeypatch, test_keys):
    monkeypatch.setattr(config, "KEYS", test_keys)
    assert config.get_key_action(Mode.BOOKS_PAGE, "esc") == "test_exit"


def test_get_mode_by_raw_value():
    assert Mode.get("КНИГИ") == Mode.BOOKS_PAGE
    assert Mode.get("НЕ СУЩЕСТВУЕТ") is None


def test_help_for_mode(monkeypatch, test_keys):
    monkeypatch.setattr(config, "KEYS", test_keys)
    result = config.help_string_for(Mode.BOOKS_PAGE)
    assert result == TEST_HELP_STRING_FOR_BOOKS_PAGE


def test_keys_actions_exists():
    actions = [k.action for k in KEYS]
    controller = ViewController()
    for action in actions:
        assert action in dir(controller)
