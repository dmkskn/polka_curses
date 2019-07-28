import urwid


class LoadingPage(urwid.WidgetWrap):
    def __init__(self):
        self.emoji = ["🌍", "🌏", "🌎"]
        w = urwid.Text("🌍", align=urwid.CENTER)
        w = urwid.Filler(w)
        super().__init__(w)

    @property
    def text(self):
        return self._w.base_widget.text

    @text.setter
    def text(self, value):
        self._w.base_widget.set_text(value)

    def update(self):
        i = self.emoji.index(self.text)  # the current emoji index
        next_i = (i + 1) % len(self.emoji)  # the next emoji index
        self.text = self.emoji[next_i]
