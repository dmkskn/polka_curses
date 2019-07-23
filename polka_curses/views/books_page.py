import urwid
from polka_curses.config import Palette as p


class BooksPage(urwid.ListBox):
    def __init__(self, books):
        self.books = books
        widgets = [BookItem(b) for b in self.books]
        super().__init__(urwid.SimpleFocusListWalker(widgets))

    def get_focused_book(self):
        widget, _ = self.get_focus()
        return widget.book


class BookItem(urwid.WidgetWrap):
    def __init__(self, book):
        self.book = book
        body = urwid.Text(self.body)
        body = urwid.Padding(body, left=1, right=1)
        item = urwid.LineBox(body, self.header, urwid.LEFT)
        super().__init__(urwid.AttrMap(item, p.frame.name, p.frame_focus.name))

    @property
    def header(self):
        return self.book.title

    @property
    def body(self):
        authors = ", ".join(self.book.authors)
        sy, ey = self.book.year
        years = f"{sy or ''}{'-' if sy and ey else ''}{ey or ''}"
        return f"{authors}{', ' if authors else ''}{years}"

    def selectable(self):
        return True
