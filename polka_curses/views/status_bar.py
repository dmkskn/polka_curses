import urwid
from urwid import LEFT, RIGHT, PACK

from polka_curses.config import Palette as p


class StatusBar(urwid.WidgetWrap):
    def __init__(self, left="", right=""):
        lcol = urwid.Text(left, align=LEFT)
        rcol = urwid.Text(right, align=RIGHT)
        cols = urwid.Columns([lcol, (PACK, rcol)], dividechars=1)
        cols = urwid.Padding(cols, left=1, right=1)
        super().__init__(urwid.AttrMap(cols, p.footer.name))

    @property
    def cols(self):
        contents = self._w.original_widget.base_widget.contents
        return (contents[0][0], contents[1][0])

    @property
    def left(self):
        return self.cols[0].text

    @property
    def right(self):
        return self.cols[1].text

    def set_left(self, text):
        self.cols[0].set_text(text)

    def set_right(self, text):
        self.cols[1].set_text(text)

    def clear_left(self):
        self.set_left("")

    def clear_right(self):
        self.set_right("")
