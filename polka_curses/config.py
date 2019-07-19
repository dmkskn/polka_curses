from enum import Enum
from typing import NamedTuple, List, Set


class Mode(Enum):
    BOOKS_PAGE = "КНИГИ"
    LISTS_PAGE = "СПИСКИ"
    EXPERTS_PAGE = "ЭКСПЕРТЫ"
    SEARCH_PAGE = "ПОИСК"
    SEARCH_RESULTS_PAGE = "РЕЗУЛЬТАТЫ ПОИСКА"

    @classmethod
    def get(cls, raw_value):
        for mode in cls:
            if mode.value == raw_value:
                return mode

    @classmethod
    def tabs(cls):
        return {
            cls.BOOKS_PAGE,
            cls.LISTS_PAGE,
            cls.EXPERTS_PAGE,
            cls.SEARCH_PAGE,
            cls.SEARCH_RESULTS_PAGE,
        }


class Palette(NamedTuple):
    name: str
    fore: str = ""
    back: str = ""
    mono: str = ""
    fore_high: str = ""
    back_high: str = ""


class Key(NamedTuple):
    """Represents a keyboard input sent by a user’s terminal.

    - `name` is a human-readable name
    - `buttons` is an input returned by Urwid
    - `action` is a method name in the controller
    - `modes` points out for which Modes this Key is relevant"""

    name: str
    description: str
    buttons: List[str]
    action: str
    modes: Set[Mode]


PALETTE = [
    Palette("frame", fore_high="#000", back_high="#fff"),
    Palette("header", fore_high="#fff", back_high="#00f"),
    Palette("footer", fore_high="#fff", back_high="#00f"),
    Palette("highlighted", fore_high="#000", back_high="#ff0"),
    Palette("highlighted_header", fore_high="#fff", back_high="#f00"),
]


KEYS = [
    Key(
        name="Left",
        description="ВЛЕВО",
        buttons=["left"],
        action="move_left",
        modes=Mode.tabs(),
    ),
    Key(
        name="Right",
        description="ВПРАВО",
        buttons=["right"],
        action="move_right",
        modes=Mode.tabs(),
    ),
    Key(
        name="Enter",
        description="ИСКАТЬ",
        buttons=["enter"],
        action="show_search_results",
        modes={Mode.SEARCH_PAGE},
    ),
    Key(
        name="Space",
        action="show_search",
        buttons=[" "],
        description="НОВЫЙ ПОИСК",
        modes={Mode.SEARCH_RESULTS_PAGE},
    ),
    Key(
        name="Esc",
        description="ВЫХОД",
        buttons=["esc"],
        action="exit",
        modes=Mode.tabs(),
    ),
]


def get_keys_by_mode(mode):
    return (key for key in KEYS if mode in key.modes)


def get_key_action(mode, key):
    for item in get_keys_by_mode(mode):
        if key in item.buttons:
            return item.action
    return None
