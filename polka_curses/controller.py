import webbrowser
from collections import deque
from functools import wraps

import urwid

from .config import Mode, Palette, help_string_for
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
        self.mode = Mode.LOADING_PAGE
        self.last_mode = deque()
        self.model = Model()
        self.view = View()
        self.loading = 10
        self.input_handler = InputHandler(self)

    def run(self):
        """Start the main loop."""
        self.loop = urwid.MainLoop(self.view)
        self.loop.handle_mouse = False
        self.loop.unhandled_input = self.input_handler.handle
        self.loop.screen.reset_default_terminal_palette()
        self.loop.screen.set_terminal_properties(256, False)
        self.loop.screen.register_palette(Palette.as_list())
        self.set_loading_page()
        self.model.get_all()
        self.loop.run()

    def exit(self):
        """Stop the main loop."""
        raise urwid.ExitMainLoop()

    def set_loading_page(self):
        callback = self.update_loading_page
        self.remove_handler = self.loop.set_alarm_in(0.2, callback)

    def remove_loading_page(self):
        self.loop.remove_alarm(self.remove_handler)

    @update
    def update_loading_page(self, *args, **kwargs):
        if self.model.is_loaded:
            self.remove_loading_page()
            rmsg = help_string_for(Mode.BOOKS_PAGE)
            self.view.init(self.model.books, rmsg=rmsg)
            self.set_mode(Mode.BOOKS_PAGE)
        else:
            self.view.update_loading_page()
            self.set_loading_page()

    def set_mode(self, mode, save_last=False):
        if save_last:
            self.last_mode.append(self.mode)
        self.mode = mode

    def get_mode(self):
        return self.mode

    def get_last_mode(self):
        return self.last_mode.pop() if self.last_mode else None

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
        self.set_mode(mode, save_last=True)

    @update
    def show_search_results(self):
        """If the results exist, show them, and if not, show a new
        search page."""
        query = self.view.get_search_query()
        results = self.model.search(query)
        if results:
            mode = Mode.SEARCH_RESULTS_PAGE
            help_string = help_string_for(mode)
            self.view.show_search_results(results, rmsg=help_string)
        else:
            mode = Mode.SEARCH_PAGE
            help_string = help_string_for(mode)
            self.view.draw_search("Нет результатов", help_string)
        self.set_mode(mode, save_last=True)

    @update
    def show_search(self):
        """Show search page."""
        mode = Mode.SEARCH_PAGE
        help_string = help_string_for(mode)
        self.view.draw_search(rmsg=help_string)
        self.set_mode(mode, save_last=True)

    @update
    def open_search_result(self):
        result = self.view.get_focused_search_result()
        if self.model.is_book(result):
            if result.has_article:
                mode = Mode.BOOK_PAGE
                rmsg = help_string_for(mode)
                self.view.draw_book(result, rmsg=rmsg)
            else:
                self.view.write_error_the_book_has_no_page(result)
                return None
        elif self.model.is_list(result):
            mode = Mode.LIST_PAGE
            rmsg = help_string_for(mode)
            self.view.draw_list(result, rmsg=rmsg)
        else:
            mode = Mode.EXPERT_PAGE
            rmsg = help_string_for(mode)
            self.view.draw_expert(result, rmsg=rmsg)
        self.set_mode(mode, save_last=True)

    @update
    def open_book(self):
        book = self.view.get_focused_book()
        if self.model.book_has_article(book):
            mode = Mode.BOOK_PAGE
            rmsg = help_string_for(mode)
            self.view.draw_book(book, rmsg=rmsg)
            self.set_mode(mode, save_last=True)
        else:
            self.view.write_error_the_book_has_no_page(book)

    @update
    def open_list(self):
        mode = Mode.LIST_PAGE
        list_ = self.view.get_focused_list()
        rmsg = help_string_for(mode)
        self.view.draw_list(list_, rmsg=rmsg)
        self.set_mode(mode, save_last=True)

    @update
    def open_expert(self):
        mode = Mode.EXPERT_PAGE
        expert = self.view.get_focused_expert()
        rmsg = help_string_for(mode)
        self.view.draw_expert(expert, rmsg=rmsg)
        self.set_mode(mode, save_last=True)

    @update
    def show_list_description(self):
        mode = Mode.LIST_DESCRIPTION_PAGE
        rmsg = help_string_for(mode)
        self.view.draw_list_description(rmsg=rmsg)
        self.set_mode(mode, save_last=True)

    @update
    def open_previous(self):
        mode = self.get_last_mode()
        if mode:
            self.view.draw_previous()
            self.set_mode(mode)

    def open_in_browser(self):
        if self.mode == Mode.BOOK_PAGE:
            url = self.view.get_book_article_url()
        elif self.mode == Mode.LIST_PAGE:
            url = self.view.get_list_article_url()
        elif self.mode == Mode.EXPERT_PAGE:
            url = self.view.get_expert_article_url()
        webbrowser.open(url)
