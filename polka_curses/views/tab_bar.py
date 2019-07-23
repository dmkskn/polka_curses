import urwid
from urwid import CENTER

from polka_curses.config import Palette as p


class TabBar(urwid.WidgetWrap):
    TABS = ["КНИГИ", " • ", "СПИСКИ", " • ", "ЭКСПЕРТЫ", " • ", "ПОИСК"]

    def __init__(self, index):
        self.index = index
        super().__init__(self._build())

    def _build(self):
        text = self.tabs
        text[self.i] = (p.header_focus.name, text[self.i])
        text = urwid.Text(text, align=CENTER)
        return urwid.AttrMap(text, p.header.name)

    def update(self):
        self._w = self._build()

    @property
    def tabs(self):
        return self.TABS.copy()

    @property
    def i(self):
        """The correct index that points out to the current tab."""
        return self.index * 2

    def _is_valid_index(self, index):
        return index >= 0 and index <= (len(self.tabs) // 2)

    def set_tab(self, index):
        if self._is_valid_index(index):
            self.index = index
            self.update()
        else:
            raise IndexError(f"tab bar index out of range")

    def get_current_tab(self):
        return self.tabs[self.i]

    def is_last_index(self):
        return self.index == (len(self.tabs) // 2)

    def is_first_index(self):
        return self.index == 0


class TitleHeader(urwid.WidgetWrap):
    def __init__(self, text):
        self.text = text
        super().__init__(self.build())

    def build(self):
        text = urwid.Text(self.text, align=CENTER)
        return urwid.AttrMap(text, p.header.name)

    @classmethod
    def init_for_book(cls, book):
        authors = ", ".join(book.authors) or None
        authors = "(" + authors + ")" if authors else ""
        authors = authors.upper()
        title = book.title.upper()
        return cls(f"{title} {authors}")

    @classmethod
    def init_for_list(cls, list_):
        title = f"{list_.title.upper()} - {list_.short_description.upper()}"
        return cls(title)

    @classmethod
    def init_for_expert(cls, expert):
        return cls(expert.name.upper())
