from .config import get_key_action


class InputHandler:
    """Maps user input to calls to `Controller` functions."""

    def __init__(self, controller):
        self.controller = controller

    def do(self, action):
        for method in dir(self.controller):
            if method == action:
                getattr(self.controller, action)()

    def handle(self, key):
        action = get_key_action(self.controller.mode, key)
        self.do(action)
