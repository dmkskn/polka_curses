import pytest
import polka
import random

from polka_curses.model import Model


BOOK_ID = 523
LIST_ID = 85
EXPERT_ID = 344


@pytest.fixture
def model():
    return Model()


@pytest.fixture
def book():
    return polka.Book(BOOK_ID)


@pytest.fixture
def not_book():
    return random.choice([polka.Compilation(LIST_ID), polka.Pundit(EXPERT_ID)])


@pytest.fixture
def expert():
    return polka.Pundit(EXPERT_ID)


@pytest.fixture
def not_expert():
    return random.choice([polka.Compilation(LIST_ID), polka.Book(BOOK_ID)])


@pytest.fixture
def list_():
    return polka.Compilation(LIST_ID)


@pytest.fixture
def not_list():
    return random.choice([polka.Pundit(EXPERT_ID), polka.Book(BOOK_ID)])


def test_get_books(model):
    assert [book is polka.Book for book in model.books]


def test_get_lists(model):
    assert [l is polka.Compilation for l in model.lists]


def test_get_experts(model):
    assert [expert is polka.Pundit for expert in model.experts]


def test_search(model):
    result, *results = polka.search("пушкин")
    assert isinstance(results, list)
    assert isinstance(result, tuple)
    assert len(result) == 3


def test_book_is_book(model, book, not_book):
    assert model.is_book(book)
    assert not model.is_book(not_book)


def test_expert_is_expert(model, expert, not_expert):
    assert model.is_expert(expert)
    assert not model.is_expert(not_expert)


def test_list_is_list(model, list_, not_list):
    assert model.is_list(list_)
    assert not model.is_list(not_list)


def test_book_has_article(model, book):
    assert model.book_has_article(book) == book.has_article
