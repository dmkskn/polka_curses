import urwid
from urwid import CENTER, RELATIVE, TOP, LEFT

from polka_curses.config import Palette as p


RELATIVE_55 = (RELATIVE, 55)
RELATIVE_90 = (RELATIVE, 90)


class SearchResultsExseption(Exception):
    pass


class SearchPage(urwid.WidgetWrap):
    def __init__(self):
        self.search = urwid.Edit()
        bg = urwid.SolidFill("⢻")
        w = urwid.Filler(urwid.LineBox(self.search, "ПОИСК 🔎", CENTER))
        w = urwid.Overlay(w, bg, CENTER, RELATIVE_55, TOP, 3, top=2)
        super().__init__(w)

    def get_search_query(self):
        return self.search.edit_text


class SearchResultsPage(urwid.WidgetWrap):
    def __init__(self, results):
        self.results = SearchResults(results)
        bg = urwid.SolidFill("⢻")
        w = urwid.LineBox(self.results, "ПОИСК 🔎", CENTER)
        w = urwid.Overlay(w, bg, CENTER, RELATIVE_55, TOP, RELATIVE_90, top=2)
        super().__init__(w)

    def get_focused_result(self):
        return self.results.get_focused_result()


class SearchResults(urwid.ListBox):
    def __init__(self, results):
        self.results = [SearchResultItem(r) for r in results]
        super().__init__(urwid.SimpleFocusListWalker(self.results))

    def get_focused_result(self):
        if self.results:
            w, _ = self.get_focus()
            return w.result.object
        else:
            raise SearchResultsExseption("there is no results")


class SearchResultItem(urwid.WidgetWrap):
    def __init__(self, result):
        self.result = result
        body = urwid.Text(self.body)
        body = urwid.Padding(body, left=1, right=1)
        item = urwid.LineBox(body, self.header, LEFT)
        super().__init__(urwid.AttrMap(item, p.frame.name, p.frame_focus.name))

    @property
    def header(self):
        return self.result.title

    @property
    def body(self):
        return f"{self.result.description}..."

    def selectable(self):
        return True
