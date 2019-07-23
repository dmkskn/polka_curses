import urwid

from polka_curses.config import Palette as p


class ListsPage(urwid.ListBox):
    def __init__(self, lists):
        self.lists = lists
        widgets = [ListItem(l) for l in self.lists]
        super().__init__(urwid.SimpleFocusListWalker(widgets))

    def get_focused_list(self):
        widget, _ = self.get_focus()
        return widget.list_


class ListItem(urwid.WidgetWrap):
    def __init__(self, list_):
        self.list_ = list_
        body = urwid.Text(self.body)
        body = urwid.Padding(body, left=1, right=1)
        item = urwid.LineBox(body, self.header, urwid.LEFT)
        super().__init__(urwid.AttrMap(item, p.frame.name, p.frame_focus.name))

    @property
    def header(self):
        return self.list_.title

    @property
    def body(self):
        return self.list_.short_description

    def selectable(self):
        return True
