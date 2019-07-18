import urwid


class ExpertsPage(urwid.ListBox):
    def __init__(self, experts):
        self.experts = experts
        widgets = [ExpertItem(b) for b in self.experts]
        super().__init__(urwid.SimpleFocusListWalker(widgets))

    def get_focused_expert(self):
        widget, _ = self.get_focus()
        return widget.expert


class ExpertItem(urwid.WidgetWrap):
    def __init__(self, expert):
        self.expert = expert
        body = urwid.Text(self.body)
        body = urwid.Padding(body, left=1, right=1)
        item = urwid.LineBox(body, self.header, urwid.LEFT)
        super().__init__(urwid.AttrMap(item, "frame", "highlighted"))

    @property
    def header(self):
        return self.expert.name

    @property
    def body(self):
        return self.expert.credit

    def selectable(self):
        return True
