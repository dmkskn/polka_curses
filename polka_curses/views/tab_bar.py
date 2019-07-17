import urwid


class TabBar(urwid.WidgetWrap):
    TABS = ["КНИГИ", " • ", "СПИСКИ", " • ", "ЭКСПЕРТЫ", " • ", "ПОИСК"]

    def __init__(self, index):
        self.index = index
        super().__init__(self._build())

    def _build(self):
        text = self.tabs
        text[self.i] = ("highlighted_header", text[self.i])
        text = urwid.Text(text, align=urwid.CENTER)
        return urwid.AttrMap(text, "header")

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
