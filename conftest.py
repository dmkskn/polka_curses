import pytest
import random
from unittest.mock import MagicMock

from polka_curses.controller import ViewController
from polka_curses.model import Model
from polka_curses.view import View
from polka_curses.config import Key, Mode


@pytest.fixture(scope="module")
def model():
    class TestModel(Model):
        def get_all(self):
            pass

    return TestModel()


@pytest.fixture(scope="module")
def books(model):
    return model.books


@pytest.fixture(scope="module")
def lists(model):
    return model.lists


@pytest.fixture(scope="module")
def experts(model):
    return model.experts


@pytest.fixture(scope="module")
def book(books):
    return books[0]


@pytest.fixture(scope="module")
def not_book(expert, list_):
    return random.choice([expert, list_])


@pytest.fixture(scope="module")
def list_(lists):
    return lists[0]


@pytest.fixture(scope="module")
def not_list(book, expert):
    return random.choice([book, expert])


@pytest.fixture(scope="module")
def expert(experts):
    return experts[0]


@pytest.fixture(scope="module")
def not_expert(book, list_):
    return random.choice([book, list_])


@pytest.fixture
def view(books):
    view = View()
    view.init(books)
    return view


@pytest.fixture
def view_with_loading_page():
    return View()


@pytest.fixture
def controller(view):
    controller = ViewController()
    controller.loop = MagicMock()
    controller.view = view
    controller.mode = Mode.BOOKS_PAGE
    return controller


@pytest.fixture
def test_keys():
    return [
        Key(
            name="Left",
            description="ВЛЕВО",
            buttons=["left"],
            action="test_move_left",
            modes=Mode.tabs(),
            hidden=True,
        ),
        Key(
            name="Enter",
            description="ОТКРЫТЬ",
            buttons=["enter"],
            action="test_open_book",
            modes=Mode.tabs(),
        ),
        Key(
            name="Esc",
            description="ВЫХОД",
            buttons=["esc"],
            action="test_exit",
            modes=Mode.tabs(),
        ),
    ]
