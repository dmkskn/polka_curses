from functools import wraps
from threading import Thread

import polka


def threaded(func):
    @wraps(func)
    def async_func(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return async_func


class Model:
    """Access to the Polka API"""

    def __init__(self):
        self._books = []
        self._lists = []
        self._experts = []
        self.is_loaded = False

    @property
    def books(self):
        """Gets list of books. Each book is an instance of polka.Book
        class."""
        if not self._books:
            self._books = polka.books()
        return self._books

    @property
    def lists(self):
        """Gets list of compilations. Each compilations is an instance
        of polka.Compilation class."""
        if not self._lists:
            self._lists = polka.lists()
        return self._lists

    @property
    def experts(self):
        """Gets list of experts. Each expert is an instance
        of polka.Pundit class."""
        if not self._experts:
            self._experts = polka.pundits()
        return self._experts

    def search(self, query):
        """Search for the `query`. Each expert is a tuple `(title,
        description, object)`."""
        return polka.search(query)

    def is_book(self, obj):
        return isinstance(obj, polka.Book)

    def is_list(self, obj):
        return isinstance(obj, polka.Compilation)

    def is_expert(self, obj):
        return isinstance(obj, polka.Pundit)

    def book_has_article(self, book: polka.Book):
        return book.has_article

    @threaded
    def get_all(self):
        """Preload all data"""
        _ = self.books
        _ = self.lists
        _ = self.experts
        self.is_loaded = True
