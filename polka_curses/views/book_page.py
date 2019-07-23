from builtins import property

import urwid

from polka_curses.views.widgets.scrollable_text import ScrollableText
from polka_curses.config import Palette as p


class BookPage(urwid.WidgetWrap):
    def __init__(self, book):
        self.book = book
        super().__init__(self.build())

    @property
    def questions(self):
        return [Question(q, a) for q, a, _ in self.book.questions]

    def build(self):
        lcol = urwid.LineBox(Questions(self.questions, self.change_answer))
        rcol = Answer("")
        self.cols = urwid.Columns([(35, lcol), rcol], focus_column=0)
        self.questions_column.update_answer()
        return self.cols

    def change_answer(self, answer):
        options = self.cols.contents[1][1]
        answer = urwid.LineBox(urwid.Padding(Answer(answer), left=1, right=1))
        answer = urwid.AttrMap(answer, p.frame.name, p.frame_focus.name)
        self.cols.contents[1] = (answer, options)

    @property
    def questions_column(self):
        return self.cols.contents[0][0].base_widget

    @property
    def answer_column(self):
        return self.cols.contents[1][0].base_widget


class Question(urwid.WidgetWrap):
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        super().__init__(self.build())

    def build(self):
        borders = {
            "tlcorner": "",
            "tline": " ",
            "lline": " ",
            "trcorner": "",
            "blcorner": "",
            "rline": " ",
            "bline": " ",
            "brcorner": "",
        }
        w = urwid.Text(self.question.upper())
        w = urwid.LineBox(w, **borders)
        return urwid.AttrMap(w, p.frame_bold.name, p.frame_bold_focus.name)

    def selectable(self):
        return True


class Questions(urwid.ListBox):
    def __init__(self, questions, func_for_changing_answer):
        self.questions = questions
        self.change_answer = func_for_changing_answer
        super().__init__(urwid.SimpleFocusListWalker(self.questions))

    def change_focus(self, *args, **kwargs):
        super().change_focus(*args, **kwargs)
        self.update_answer()

    def update_answer(self):
        self.change_answer(self.focus.answer)


class Answer(ScrollableText):
    pass
