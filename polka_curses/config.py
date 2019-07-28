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
    LIST_DESCRIPTION_PAGE = "ИНФОРМАЦИЯ О СПИСКЕ"
    LOADING_PAGE = "СТРАНИЦА ЗАГРУЗКИ"

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


WHITE = "#fff"
BLACK = "#000"
BLUE = "#00f"
YELLOW = "#ff0"
RED = "#f00"
BOLD = "bold"


class PaletteItem(NamedTuple):
    name: str
    fore: str = ""
    back: str = ""
    mono: str = ""
    fore_high: str = ""
    back_high: str = ""


class Palette(Enum):
    header = PaletteItem("header", fore_high=WHITE, back_high=BLUE)
    header_focus = PaletteItem("header_focus", fore_high=WHITE, back_high=RED)
    footer = PaletteItem("footer", fore_high=WHITE, back_high=BLUE)
    footer_error = PaletteItem("footer_error", fore_high=WHITE, back_high=RED)
    frame = PaletteItem("frame", fore_high=BLACK, back_high=WHITE)
    frame_focus = PaletteItem("frame_focus", fore_high=BLACK, back_high=YELLOW)
    frame_bold = PaletteItem(
        "frame_bold", fore_high=f"{BOLD},{BLACK}", back_high=WHITE
    )
    frame_bold_focus = PaletteItem(
        "frame_bold_focus", fore_high=f"{BOLD},{BLACK}", back_high=YELLOW
    )

    @classmethod
    def as_list(cls):
        return [p.value for p in cls]


class Key(NamedTuple):
    """Represents a keyboard input sent by a user’s terminal."""

    name: str
    description: str
    buttons: List[str]
    action: str
    modes: Set[Mode]
    hidden: bool = False


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
        name="Space",
        buttons=[" "],
        action="show_list_description",
        description="ОПИСАНИЕ",
        modes={Mode.LIST_PAGE},
    ),
    Key(
        name="Space",
        buttons=[" "],
        action="open_previous",
        description="ЗАКРЫТЬ",
        modes={Mode.LIST_DESCRIPTION_PAGE},
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
        name="Tab",
        buttons=["tab"],
        action="open_in_browser",
        description="ОТКРЫТЬ В БРАУЗЕРЕ",
        modes=Mode.pages(),
    ),
    Key(
        name="Enter",
        buttons=["enter"],
        action="open_search_result",
        description="ОТКРЫТЬ",
        modes={Mode.SEARCH_RESULTS_PAGE},
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
        modes=Mode.tabs().union({Mode.LOADING_PAGE}),
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
