import pytest

from polka_curses.views.book_page import BookPage, Questions, Question, Answer


@pytest.fixture
def bookpage(book):
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
