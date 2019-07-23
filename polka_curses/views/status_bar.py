import urwid
from urwid import LEFT, RIGHT, PACK

from polka_curses.config import Palette as p


class StatusBar(urwid.WidgetWrap):
    def __init__(self, left="", right=""):
        lcol = urwid.Text(left, align=LEFT)
        rcol = urwid.Text(right, align=RIGHT)
        cols = urwid.Columns([lcol, (PACK, rcol)], dividechars=1)
        super().__init__(urwid.AttrMap(cols, p.footer.name))

    @property
    def cols(self):
        return self._w.original_widget.base_widget.contents

    @property
    def left(self):
        return self.cols[0][0].base_widget.text

    @property
    def right(self):
        return self.cols[1][0].base_widget.text

    def set_left(self, text, error=False):
        if error:
            text = urwid.AttrMap(urwid.Text(text), p.footer_error.name)
        else:
            text = urwid.AttrMap(urwid.Text(text), p.footer.name)
        cols = self._w.original_widget.base_widget
        cols.contents[0] = (text, cols.contents[0][1])

    def set_right(self, text):
        text = urwid.AttrMap(urwid.Text(text), p.footer.name)
        cols = self._w.original_widget.base_widget
        cols.contents[1] = (text, cols.contents[1][1])

    def clear_left(self):
        self.set_left("")

    def clear_right(self):
        self.set_right("")
