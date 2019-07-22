import urwid


BOOK_BODY_TEMPLATE = """
{authors}{sep}{years}

{desc}
"""


class ListPage(urwid.ListBox):
    def __init__(self, list_):
        self.list_ = list_
        widgets = [BookInListItem(b) for b in self.list_.books]
        super().__init__(urwid.SimpleFocusListWalker(widgets))

    def get_focused_book(self):
        widget, _ = self.get_focus()
        return widget.book


class BookInListItem(urwid.WidgetWrap):
    def __init__(self, book):
        self.book = book
        body = urwid.Padding(self.body, left=1, right=1)
        item = urwid.LineBox(body, self.header, urwid.LEFT)
        super().__init__(urwid.AttrMap(item, "frame", "highlighted"))

    @property
    def header(self):
        return self.book.title

    @property
    def body(self):
        authors = ", ".join(self.book.authors)
        sy, ey = self.book.year
        years = f"{sy or ''}{'-' if sy and ey else ''}{ey or ''}"
        sep = ", " if authors else ""
        desc = self.book.description
        return urwid.Text(f"\n{authors}{sep}{years}\n\n{desc}")

    def selectable(self):
        return True
