import urwid

from .config import PALETTE, Mode
from .handler import InputHandler


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
