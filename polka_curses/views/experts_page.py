import urwid
from urwid import LEFT

from polka_curses.config import Palette as p


class ExpertsPage(urwid.ListBox):
    def __init__(self, experts):
        self.experts = experts
        widgets = [ExpertItem(e) for e in self.experts]
        super().__init__(urwid.SimpleFocusListWalker(widgets))

    def get_focused_expert(self):
        widget, _ = self.get_focus()
        return widget.expert


class ExpertItem(urwid.WidgetWrap):
    def __init__(self, expert):
        self.expert = expert
        body = urwid.Text(self.body)
        body = urwid.Padding(body, left=1, right=1)
        item = urwid.LineBox(body, self.header, LEFT)
        super().__init__(urwid.AttrMap(item, p.frame.name, p.frame_focus.name))

    @property
    def header(self):
        return self.expert.name

    @property
    def body(self):
        return self.expert.credit

    def selectable(self):
        return True
