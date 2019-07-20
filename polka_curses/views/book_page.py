import urwid

from polka_curses.views.widgets.scrollable_text import ScrollableText


class BookPage(urwid.WidgetWrap):
    def __init__(self, book):
        self.book = book
        super().__init__(self.build())

    @property
    def questions(self):
        return [Question(q, a) for q, a, _ in self.book.questions]

    def build(self):
        self.answer_column = Answer("")
        self.questions_column = Questions(self.questions, self.answer_column)
        self.questions_column.update_answer()

        lcol = urwid.LineBox(self.questions_column)
        rcol = urwid.Padding(self.answer_column, left=1, right=1)
        rcol = urwid.LineBox(rcol)

        return urwid.Columns([(35, lcol), rcol], focus_column=0)


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
        return urwid.AttrMap(w, "frame_bold", "highlighted_bold")

    def selectable(self):
        return True


class Questions(urwid.ListBox):
    def __init__(self, questions, answer_column):
        self.questions = questions
        self.answer_column = answer_column
        super().__init__(urwid.SimpleFocusListWalker(self.questions))

    def change_focus(self, *args, **kwargs):
        super().change_focus(*args, **kwargs)
        self.update_answer()

    def update_answer(self):
        self.answer_column.set_text(self.focus.answer)


class Answer(ScrollableText):
    pass
