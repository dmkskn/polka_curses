import urwid

from .views.books_page import BooksPage
from .views.tab_bar import TabBar
from .views.status_bar import StatusBar


class View(urwid.WidgetWrap):
    def __init__(self, books, left_message="", right_message=""):
        books = BooksPage(books)
        tabbar = TabBar(0)
        statusbar = StatusBar(left_message, right_message)
        self.frame = urwid.Frame(books, tabbar, statusbar)
        super().__init__(urwid.AttrMap(self.frame, "frame"))
