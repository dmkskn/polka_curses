import urwid

from .views.books_page import BooksPage
from .views.lists_page import ListsPage
from .views.experts_page import ExpertsPage
from .views.book_page import BookPage
from .views.list_page import ListPage
from .views.expert_page import ExpertPage
from .views.search_page import SearchPage, SearchResultsPage
from .views.tab_bar import TabBar, TitleHeader
from .views.status_bar import StatusBar


class View(urwid.WidgetWrap):
    """It is intended for managing the UI views."""

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
        """Replaces the body with a `BooksPage` object and the frame
        footer with a new `StatusBar` object."""
        self.set_body(BooksPage(books))
        self.set_footer(StatusBar(lmsg, rmsg))

    def draw_lists(self, lists, lmsg="", rmsg=""):
        """Replaces the body with a `ListsPage` object and the frame
        footer with a new `StatusBar` object."""
        self.set_body(ListsPage(lists))
        self.set_footer(StatusBar(lmsg, rmsg))

    def draw_experts(self, experts, lmsg="", rmsg=""):
        """Replaces the body with an `ExpertsPage` object and the frame
        footer with a new `StatusBar` object."""
        self.set_body(ExpertsPage(experts))
        self.set_footer(StatusBar(lmsg, rmsg))

    def draw_search(self, lmsg="", rmsg=""):
        """Replaces the body with a `SearchPage` object and the frame
        footer with a new `StatusBar` object."""
        self.set_body(SearchPage())
        self.set_footer(StatusBar(lmsg, rmsg))

    def show_search_results(self, results, lmsg="", rmsg=""):
        """Replaces the body with a `SearchResultsPage` object and
        the frame footer with a new `StatusBar` object."""
        self.set_body(SearchResultsPage(results))
        self.set_footer(StatusBar(lmsg, rmsg))

    def get_search_query(self):
        """Returns the search query from a `SearchResultsPage` object"""
        return self.body.get_search_query()

    def focus_previous_tab(self):
        """Focuses the previous tab in the header."""
        if not self.header.is_first_index():
            self.header.set_tab(self.header.index - 1)
            self.footer.clear_left()
        return self.header.get_current_tab()

    def focus_next_tab(self):
        """Focuses the next tab in the header."""
        if not self.header.is_last_index():
            self.header.set_tab(self.header.index + 1)
            self.footer.clear_left()
        return self.header.get_current_tab()

    def get_focused_list(self):
        return self.body.get_focused_list()

    def get_focused_book(self):
        return self.body.get_focused_book()

    def get_focused_expert(self):
        return self.body.get_focused_expert()

    def get_focused_search_result(self):
        return self.body.get_focused_result()

    def draw_book(self, book, left_message="", right_message=""):
        """Replaces the body with a `BookPage` object and
        the frame footer with a new `StatusBar` object."""
        self.set_body(BookPage(book))
        self.set_footer(StatusBar(left_message, right_message))
        self.set_header(TitleHeader.init_for_book(book))

    def draw_list(self, list_, left_message="", right_message=""):
        """Replaces the body with a `ListPage` object and
        the frame footer with a new `StatusBar` object."""
        self.set_body(ListPage(list_))
        self.set_footer(StatusBar(left_message, right_message))
        self.set_header(TitleHeader.init_for_list(list_))

    def draw_expert(self, expert, left_message="", right_message=""):
        """Replaces the body with an `ExpertPage` object and
        the frame footer with a new `StatusBar` object."""
        self.set_body(ExpertPage(expert))
        self.set_footer(StatusBar(left_message, right_message))
        self.set_header(TitleHeader.init_for_expert(expert))

    def write_error_the_book_has_no_page(self, book):
        text = f"Нет статьи на книгу «{book.title.upper()}»"
        self.footer.set_left(text)
