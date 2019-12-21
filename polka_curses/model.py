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
        self._podcasts = []
        self._blogs = []
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

    @property
    def podcasts(self):
        """Gets list of podcasts. Each podcast is an instance
        od polka.Podcast class."""
        if not self._podcasts:
            self._podcasts = polka.podcasts()
        return self._podcasts

    @property
    def blogs(self):
        """Gets list of blog articles. Each article is an instance
        od polka.Blog class."""
        if not self._blogs:
            self._blogs = polka.blogs()
        return self._blogs

    def is_book(self, obj):
        return isinstance(obj, polka.Book)

    def is_list(self, obj):
        return isinstance(obj, polka.Compilation)

    def is_expert(self, obj):
        return isinstance(obj, polka.Pundit)

    def is_podcast(self, obj):
        return isinstance(obj, polka.Podcast)

    def is_blog(self, obj):
        return isinstance(obj, polka.Blog)

    def book_has_article(self, book: polka.Book):
        return book.has_article

    @threaded
    def get_all(self):
        """Preload all data"""
        _ = self.books
        _ = self.lists
        _ = self.experts
        _ = self.podcasts
        _ = self.blogs
        self.is_loaded = True
