from functools import wraps

import urwid

from .config import PALETTE, Mode
from .handler import InputHandler


def update(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.loop.draw_screen()

    return wrapper


class ViewController:
    def __init__(self, view, model):
        self.model = model()
        self.view = view(self.model.books)
        self.mode = Mode.BOOKS_PAGE
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
        tab_name = self.view.focus_next_tab()
        self.draw_body_by_tab_name(tab_name)

    def move_left(self):
        tab_name = self.view.focus_prev_tab()
        self.draw_body_by_tab_name(tab_name)

    @update
    def draw_body_by_tab_name(self, tab_name):
        mode = Mode.get(tab_name)
        if mode == Mode.BOOKS_PAGE:
            self.view.draw_books(self.model.books)
        elif mode == Mode.LISTS_PAGE:
            self.view.draw_lists(self.model.lists)
        elif mode == Mode.EXPERTS_PAGE:
            self.view.draw_experts(self.model.experts)
        else:
            self.view.draw_search()
        self.mode = mode

    @update
    def show_search_results(self):
        query = self.view.get_search_query()
        results = self.model.search(query)
        if results:
            self.mode = Mode.SEARCH_RESULTS_PAGE
            self.view.show_search_results(results)
        else:
            self.mode = Mode.SEARCH_PAGE
            self.view.draw_search(lmsg="Нет результатов")

    @update
    def show_search(self):
        """Show search page."""
        self.mode = Mode.SEARCH_PAGE
        self.view.draw_search()
