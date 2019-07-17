import urwid


class ViewController:
    def __init__(self, view, model):
        self.model = model()
        self.view = view(self.model.books)

    def run(self):
        """Start the main loop."""
        self.loop = urwid.MainLoop(self.view)
        self.loop.run()

    def exit(self):
        """Stop the main loop."""
        raise urwid.ExitMainLoop()
