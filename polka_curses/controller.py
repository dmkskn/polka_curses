import urwid

from .config import PALETTE


class ViewController:
    def __init__(self, view, model):
        self.model = model()
        self.view = view(self.model.books)

    def run(self):
        """Start the main loop."""
        self.loop = urwid.MainLoop(self.view)
        self.loop.handle_mouse = False
        self.loop.screen.reset_default_terminal_palette()
        self.loop.screen.set_terminal_properties(256, False)
        self.loop.screen.register_palette(PALETTE)
        self.loop.run()

    def exit(self):
        """Stop the main loop."""
        raise urwid.ExitMainLoop()
