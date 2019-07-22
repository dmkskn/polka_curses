from functools import wraps

import urwid

from .config import PALETTE, Mode, help_string_for
from .handler import InputHandler
from .model import Model
from .view import View


def update(func):
    """Updates the screen."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.loop.draw_screen()

    return wrapper


class ViewController:
    """The core of the program. It have methods that give commands to
    the `View` and have access to the Polka API through the `Model`."""

    def __init__(self):
        self.mode = Mode.BOOKS_PAGE
        self.model = Model()
        self.view = View(self.model.books, rmsg=help_string_for(self.mode))
        self.input_handler = InputHandler(self)

    def run(self):
        """Start the main loop."""
        self.loop = urwid.MainLoop(self.view)
        self.loop.handle_mouse = False
        self.loop.unhandled_input = self.input_handler.handle
        self.loop.screen.reset_default_terminal_palette()
        self.loop.screen.set_terminal_properties(256, False)
        self.loop.screen.register_palette(PALETTE)
        self.loop.run()

    def exit(self):
        """Stop the main loop."""
        raise urwid.ExitMainLoop()

    def move_right(self):
        """Go to the next tab on the right."""
        tab_name = self.view.focus_next_tab()
        self.draw_body_by_tab_name(tab_name)

    def move_left(self):
        """Go to the previous tab on the left."""
        tab_name = self.view.focus_previous_tab()
        self.draw_body_by_tab_name(tab_name)

    @update
    def draw_body_by_tab_name(self, tab_name):
        mode = Mode.get(tab_name)
        help_string = help_string_for(mode)
        if mode == Mode.BOOKS_PAGE:
            self.view.draw_books(self.model.books, rmsg=help_string)
        elif mode == Mode.LISTS_PAGE:
            self.view.draw_lists(self.model.lists, rmsg=help_string)
        elif mode == Mode.EXPERTS_PAGE:
            self.view.draw_experts(self.model.experts, rmsg=help_string)
        else:
            self.view.draw_search(rmsg=help_string)
        self.mode = mode

    @update
    def show_search_results(self):
        """If the results exist, show them, and if not, show a new
        search page."""
        query = self.view.get_search_query()
        results = self.model.search(query)
        if results:
            self.mode = Mode.SEARCH_RESULTS_PAGE
            help_string = help_string_for(self.mode)
            self.view.show_search_results(results, rmsg=help_string)
        else:
            self.mode = Mode.SEARCH_PAGE
            help_string = help_string_for(self.mode)
            self.view.draw_search("Нет результатов", help_string)

    @update
    def show_search(self):
        """Show search page."""
        self.mode = Mode.SEARCH_PAGE
        help_string = help_string_for(self.mode)
        self.view.draw_search(rmsg=help_string)

    @update
    def open_book(self):
        book = self.view.get_focused_book()
        if self.model.book_has_article(book):
            self.mode = Mode.BOOK_PAGE
            right_message = help_string_for(self.mode)
            self.view.draw_book(book, right_message=right_message)
        else:
            self.view.write_error_the_book_has_no_page(book)

    @update
    def open_list(self):
        self.mode = Mode.LIST_PAGE
        list_ = self.view.get_focused_list()
        right_message = help_string_for(self.mode)
        self.view.draw_list(list_, right_message=right_message)

    @update
    def open_expert(self):
        self.mode = Mode.EXPERT_PAGE
        expert = self.view.get_focused_expert()
        right_message = help_string_for(self.mode)
        self.view.draw_expert(expert, right_message=right_message)
