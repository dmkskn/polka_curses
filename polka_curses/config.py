from enum import Enum
from typing import NamedTuple, List, Set


class Mode(Enum):
    """The state in which the program is running."""

    BOOKS_PAGE = "КНИГИ"
    LISTS_PAGE = "СПИСКИ"
    EXPERTS_PAGE = "ЭКСПЕРТЫ"
    SEARCH_PAGE = "ПОИСК"
    SEARCH_RESULTS_PAGE = "РЕЗУЛЬТАТЫ ПОИСКА"
    BOOK_PAGE = "СТАТЬЯ"
    LIST_PAGE = "СПИСОК"
    EXPERT_PAGE = "ЭКСПЕРТ"

    @classmethod
    def get(cls, raw_value):
        for mode in cls:
            if mode.value == raw_value:
                return mode

    @classmethod
    def pages(cls):
        return {cls.BOOK_PAGE, cls.LIST_PAGE, cls.EXPERT_PAGE}

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
    """Represents a keyboard input sent by a user’s terminal."""

    name: str
    description: str
    buttons: List[str]
    action: str
    modes: Set[Mode]
    hidden: bool = False


PALETTE = [
    Palette("frame", fore_high="#000", back_high="#fff"),
    Palette("frame_bold", fore_high="bold,#000", back_high="#fff"),
    Palette("header", fore_high="#fff", back_high="#00f"),
    Palette("footer", fore_high="#fff", back_high="#00f"),
    Palette("highlighted", fore_high="#000", back_high="#ff0"),
    Palette("highlighted_header", fore_high="#fff", back_high="#f00"),
    Palette("highlighted_bold", fore_high="bold,#000", back_high="#ff0"),
]


KEYS = [
    Key(
        name="Left",
        description="ВЛЕВО",
        buttons=["left"],
        action="move_left",
        modes=Mode.tabs(),
        hidden=True,
    ),
    Key(
        name="Right",
        description="ВПРАВО",
        buttons=["right"],
        action="move_right",
        modes=Mode.tabs(),
        hidden=True,
    ),
    Key(
        name="Enter",
        buttons=["enter"],
        action="open_book",
        description="ОТКРЫТЬ",
        modes={Mode.BOOKS_PAGE, Mode.LIST_PAGE, Mode.EXPERT_PAGE},
    ),
    Key(
        name="Enter",
        buttons=["enter"],
        action="open_list",
        description="ОТКРЫТЬ",
        modes={Mode.LISTS_PAGE},
    ),
    Key(
        name="Enter",
        buttons=["enter"],
        action="open_expert",
        description="ОТКРЫТЬ",
        modes={Mode.EXPERTS_PAGE},
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
        buttons=["esc"],
        action="open_previous",
        description="ЗАКРЫТЬ",
        modes=Mode.pages(),
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
    """Filtres `KEYS` by mode."""
    return (key for key in KEYS if mode in key.modes)


def get_key_action(mode, button):
    """Extracts the controller method name from a Key."""
    for item in get_keys_by_mode(mode):
        if button in item.buttons:
            return item.action
    return None


def help_string_for(mode):
    """Returns a string like `"ВЫХОД (Esc), ОТКРЫТЬ (Enter), ..."`."""
    keys = get_keys_by_mode(mode)
    keys = [f"{k.description} ({k.name})" for k in keys if not k.hidden]
    keys = ", ".join(keys)
    return keys
