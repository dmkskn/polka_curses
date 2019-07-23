import urwid
from urwid import PACK

from .books_page import BooksPage


class ExpertPage(urwid.WidgetWrap):
    def __init__(self, expert):
        self.expert = expert
        self.is_two_columns = expert.favorites and expert.wrote_about
        self.favorites = self.build_favorites()  # type: BooksPage
        self.wrote_about = self.build_wrote_about()  # type: BooksPage
        self.columns = {0: self.favorites, 1: self.wrote_about}
        super().__init__(self.build())

    def build(self):
        if self.is_two_columns:
            favorites = urwid.LineBox(self.favorites, title="ВЫБОР ЭКСПЕРТА")
            wrote_about = urwid.LineBox(self.wrote_about, title="СТАТЬИ")
            self.container = urwid.Columns([favorites, wrote_about], 1, 0)
        elif self.favorites:
            favorites = urwid.LineBox(self.favorites, title="ВЫБОР ЭКСПЕРТА")
            self.container = favorites
        elif self.wrote_about:
            wrote_about = urwid.LineBox(self.wrote_about, title="СТАТЬИ")
            self.container = wrote_about
        else:
            self.container = urwid.Filler(urwid.Text(""))
        return urwid.Pile([(PACK, self.description), self.container])

    def build_favorites(self):
        if self.expert.favorites:
            return BooksPage(self.expert.favorites)
        else:
            return None

    def build_wrote_about(self):
        if self.expert.wrote_about:
            return BooksPage(self.expert.wrote_about)
        else:
            return None

    @property
    def description(self):
        desc = urwid.Text(self.expert.description)
        desc = urwid.Padding(desc, left=1, right=1)
        return urwid.LineBox(desc)

    def get_focused_book(self):
        column = self.get_focused_column()
        return column.get_focused_book()

    def get_focused_column(self):
        if self.is_two_columns:
            return self.columns[self.container.focus_position]
        return self.favorites or self.wrote_about
