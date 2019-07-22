import pytest

from polka_curses.views.book_page import BookPage, Questions, Question, Answer
from polka_curses.model import Model


@pytest.fixture
def model():
    return Model()


@pytest.fixture
def bookpage(model):
    book = model.books[0]
    return BookPage(book)


def test_get_book_from_page(bookpage):
    assert bookpage.book


def test_get_questions(bookpage):
    questions = bookpage.questions
    assert isinstance(questions, list)
    assert isinstance(questions[0], Question)


def test_left_column_is_questions(bookpage):
    assert isinstance(bookpage.questions_column.base_widget, Questions)


def test_right_column_is_answer(bookpage):
    assert isinstance(bookpage.answer_column.base_widget, Answer)


def test_right_column_contains_answer_on_focused_question(bookpage):
    questions = bookpage.questions_column.base_widget
    answer = bookpage.answer_column.base_widget
    question = questions.focus
    assert question.answer == answer.text
