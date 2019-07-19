import urwid

from .views.books_page import BooksPage
from .views.lists_page import ListsPage
from .views.experts_page import ExpertsPage
from .views.search_page import SearchPage, SearchResultsPage
from .views.tab_bar import TabBar
from .views.status_bar import StatusBar


class View(urwid.WidgetWrap):
    def __init__(self, books, lmsg="", rmsg=""):
        books = BooksPage(books)
        tabbar = TabBar(0)
        statusbar = StatusBar(lmsg, rmsg)
        self.frame = urwid.Frame(books, tabbar, statusbar)
        super().__init__(urwid.AttrMap(self.frame, "frame"))

    @property
    def header(self):
        return self.frame.header

    @property
    def body(self):
        return self.frame.body

    @property
    def footer(self):
        return self.frame.footer

    def set_body(self, body):
        self.frame.set_body(body)

    def set_header(self, header):
        self.frame.set_header(header)

    def set_footer(self, footer):
        self.frame.set_footer(footer)

    def draw_books(self, books, lmsg="", rmsg=""):
        self.set_body(BooksPage(books))
        self.set_footer(StatusBar(lmsg, rmsg))

    def draw_lists(self, lists, lmsg="", rmsg=""):
        self.set_body(ListsPage(lists))
        self.set_footer(StatusBar(lmsg, rmsg))

    def draw_experts(self, experts, lmsg="", rmsg=""):
        self.set_body(ExpertsPage(experts))
        self.set_footer(StatusBar(lmsg, rmsg))

    def draw_search(self, lmsg="", rmsg=""):
        self.set_body(SearchPage())
        self.set_footer(StatusBar(lmsg, rmsg))

    def show_search_results(self, results, lmsg="", rmsg=""):
        self.set_body(SearchResultsPage(results))
        self.set_footer(StatusBar(lmsg, rmsg))

    def get_search_query(self):
        return self.body.get_search_query()

    def focus_prev_tab(self):
        if not self.header.is_first_index():
            self.header.set_tab(self.header.index - 1)
            self.footer.clear_left()
        return self.header.get_current_tab()

    def focus_next_tab(self):
        if not self.header.is_last_index():
            self.header.set_tab(self.header.index + 1)
            self.footer.clear_left()
        return self.header.get_current_tab()
