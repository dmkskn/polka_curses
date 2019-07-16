from .controller import ViewController
from .model import Model
from .view import View


def main():
    controller = ViewController(View, Model)
    controller.run()
