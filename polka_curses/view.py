from collections import deque
from functools import wraps

import urwid

from polka_curses.views.search_page import SearchResultsPage

from .config import Palette as p
from .views.book_page import BookPage
from .views.books_page import BooksPage
from .views.expert_page import ExpertPage
from .views.experts_page import ExpertsPage
from .views.list_page import ListDescription, ListPage
from .views.lists_page import ListsPage
from .views.loading_page import LoadingPage
from .views.search_page import SearchPage, SearchResultsPage
from .views.status_bar import StatusBar
from .views.tab_bar import TabBar, TitleHeader


def save_previous(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.previous_bodies.append(self.body)
        self.previous_footers.append(self.footer)
        self.previous_headers.append(self.header)
        return func(self, *args, **kwargs)

    return wrapper


def in_pages(*pages):
    """A decorator for View's methods. If a method was called and the
    current body class is not in `pages` the decorator raises an error.
    Use it only if specific objects are expected inside the method."""

    def inner(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.body, tuple(pages)):
                raise ViewError.wrong_body(self.body, pages)
            return func(self, *args, **kwargs)

        return wrapper

    return inner


class ViewError(Exception):
    @classmethod
    def wrong_body(cls, got, expected):
        got = got.__class__.__name__
        expected = [e.__name__ for e in expected]
        return cls(f"Wrong body object: {got}. Expected: {expected}")


class View(urwid.WidgetWrap):
    """It is intended for managing the UI views."""

    def __init__(self):
        self.frame = urwid.Frame(LoadingPage())
        self.previous_headers = deque()
        self.previous_bodies = deque()
        self.previous_footers = deque()
        super().__init__(urwid.AttrMap(self.frame, p.frame.name))

    @in_pages(LoadingPage)
    def update_loading_page(self):
        self.body.update()

    def init(self, books, lmsg="", rmsg=""):
        self.set_body(BooksPage(books))
        self.set_header(TabBar(0))
        self.set_footer(StatusBar(lmsg, rmsg))

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

    @in_pages(SearchPage)
    def get_search_query(self):
        """Returns the search query from a `SearchResultsPage` object"""
        return self.body.get_search_query()

    @in_pages(BooksPage, ListsPage, ExpertsPage, SearchPage, SearchResultsPage)
    def focus_previous_tab(self):
        """Focuses the previous tab in the header."""
        if not self.header.is_first_index():
            self.header.set_tab(self.header.index - 1)
            self.footer.clear_left()
        return self.header.get_current_tab()

    @in_pages(BooksPage, ListsPage, ExpertsPage, SearchPage, SearchResultsPage)
    def focus_next_tab(self):
        """Focuses the next tab in the header."""
        if not self.header.is_last_index():
            self.header.set_tab(self.header.index + 1)
            self.footer.clear_left()
        return self.header.get_current_tab()

    @in_pages(ListsPage)
    def get_focused_list(self):
        return self.body.get_focused_list()

    @in_pages(BooksPage, ListPage, ExpertPage)
    def get_focused_book(self):
        return self.body.get_focused_book()

    @in_pages(ExpertsPage)
    def get_focused_expert(self):
        return self.body.get_focused_expert()

    @in_pages(SearchResultsPage)
    def get_focused_search_result(self):
        return self.body.get_focused_result()

    @save_previous
    def draw_book(self, book, lmsg="", rmsg=""):
        """Replaces the body with a `BookPage` object and
        the frame footer with a new `StatusBar` object."""
        self.set_body(BookPage(book))
        self.set_footer(StatusBar(lmsg, rmsg))
        self.set_header(TitleHeader.init_for_book(book))

    @save_previous
    def draw_list(self, list_, lmsg="", rmsg=""):
        """Replaces the body with a `ListPage` object and
        the frame footer with a new `StatusBar` object."""
        self.set_body(ListPage(list_))
        self.set_footer(StatusBar(lmsg, rmsg))
        self.set_header(TitleHeader.init_for_list(list_))

    @save_previous
    def draw_expert(self, expert, lmsg="", rmsg=""):
        """Replaces the body with an `ExpertPage` object and
        the frame footer with a new `StatusBar` object."""
        self.set_body(ExpertPage(expert))
        self.set_footer(StatusBar(lmsg, rmsg))
        self.set_header(TitleHeader.init_for_expert(expert))

    @save_previous
    @in_pages(ListPage)
    def draw_list_description(self, lmsg="", rmsg=""):
        self.set_body(ListDescription(self.body.list_, bg=self.body))
        self.set_footer(StatusBar(lmsg, rmsg))

    def write_error_the_book_has_no_page(self, book):
        text = f"Нет статьи на книгу «{book.title.upper()}»"
        self.footer.set_left(text, error=True)

    def draw_previous(self):
        if self.previous_bodies:
            self.set_body(self.previous_bodies.pop())
        if self.previous_footers:
            self.set_footer(self.previous_footers.pop())
            self.footer.clear_left()
        if self.previous_headers:
            self.set_header(self.previous_headers.pop())

    @in_pages(BookPage)
    def get_book_article_url(self):
        return self.body.book.url

    @in_pages(ListPage)
    def get_list_article_url(self):
        return self.body.list_.url

    @in_pages(ExpertPage)
    def get_expert_article_url(self):
        return self.body.expert.url
